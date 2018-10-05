#!/usr/bin/env python
# encoding: utf-8

import os, json, time, traceback
import redis
from sqlservice import *
from tools.SYSTEM.os_ import *
from tools.SYSTEM.threading_ import  *
from tools.EXT.filter import Dicomfilter
from pulldata import *
from constants import config_obj, out, err
from multiprocessing import cpu_count,Process,JoinableQueue

from dcmlib.desensitize import desensitize_dir,is_desensitized

CNT = 1 

def get_request_json(patid, image_path, save_path):
    """
    生成请求dl server分析的json格式
    :param patid: 影像号
    :param path: 本地路径
    :return:
    """
    hjson = {}
    hjson['patid']= patid
    hjson['image_path']= image_path
    hjson['save_path']= save_path
    return hjson

def send_analysis_request(redis_client, channel, hjson):
    """
    通过redis，向dl server发送分析指定检查号的DICOM文件夹命令
    :param redis_client:
    :param channel:
    :param hjson:
    """
    redis_client.publish(channel, json.dumps(hjson))

@async
def receive_analysis_response(redis_client, channel):
    """
    接收分析返回
    :param redis_client:
    :param channel:
    :return:
    """
    try:
        ps = redis_client.pubsub()
        ps.subscribe(channel)
        for item in ps.listen():
            print item
            if item['type'] == 'message':
                if item['data'].lower() == "kill":
                    break
                else:
                    hjson = json.loads(item['data'])
                    patid = hjson['patid']
                    predict = hjson['predict']
                    if select_patient_rows(patid) > 0:
                        update_patient_predict_information(predict) #更新病人预测信息
                        out("预测结果更新TXDB成功 {}".format(patid))
                    else:
                        out("预测结果更新TXDB失败，数据库ID匹配不成功 {}".format(patid))
    except:
        out("receive predict message err")
        err(traceback.print_exc())

def service(redis_client, channel, patient,TEST):
    """
    预测当前病人
    :param redis_client:
    :param channel:
    :param patient:
    """
    try:
        patient_id = patient[0]
        #print patient
        out("start download image for patid {}".format(patient_id))

        if TEST:
            time.sleep(10)
            redis_client.set(patient_id, "", ex=24 * 60 * 60 * 2)
        # 正式使用改成True
        elif True:
            outpath = os.path.join(config_obj.STORE.dicom_store.value, patient_id)  # 文件存储地址
            save_path = os.path.join(config_obj.STORE.image_store.value, patient_id)  # 预测结果保存路径

            # 四种取病人dicom方式，四选一
            if True:
                dicompath = patient[1]
                file_number = ftp_download(config_obj.FTP, dicompath, outpath)  # FTP 下载病人dicom
            else:
                file_number = 0
                out("Choose a way that you want to achieve !")

            if file_number > 150: # number > X
                out("download image count {} {}".format(file_number, patient_id))
                redis_client.set(patient_id, outpath, ex=24*60*60*2)
                #Dicomfilter().CT(outpath)# 过滤病人dicom
                #gdcmconv(outpath) #解压dicom
                desensitize_dir(outpath)
                hjson = get_request_json(patient_id, outpath, save_path)
                send_analysis_request(redis_client, channel, hjson) # 发信预测信号到dlserver
                out("the sending channl succeed for patid {}".format(patient_id))
            else:
                out("the sending channl failed ,download image count {} patid is {}".format(file_number, patient_id))
    except:
        out("service run err {}".format(patient_id))
        err(traceback.print_exc())

def Worker(redis_client,TEST):
    while True:
        item = q.get()
        if item is None:
            break
        service(redis_client,item[0],item[1],TEST)
        q.task_done()

def Multi(redis_client, channel, patient_list,TEST):
    """
    开始获取符合条件的病人，进行预测
    :param redis_client:
    :param channel:
    :return:
    """
    try:
        starttime = time.time()
        cpuCount = cpu_count()  # 计算本机CPU核数
        #cpuCount = 3
        multiprocessing = []

        for i in xrange(0, cpuCount):  # 创建cpu_count()个进程
            p = Process(target=Worker, args=(redis_client, TEST))
            p.daemon = True
            p.start()
            multiprocessing.append(p)

        global CNT
        for i in range(len(patient_list)):
            q.put([channel+str(CNT%channelCount), patient_list[i]])
            CNT += 1
        q.join()

        for i in xrange(0, cpuCount):
            q.put(None)
        for p in multiprocessing:
            p.join()

        elapsed = (time.time() - starttime)
        out("cpuCount: {} Finished with time:{}".format(cpuCount, elapsed))

    except:
        out("Multi run error")
        err(traceback.print_exc())

#----------------------------------------------------------------------------------------------------
def get_patient_dicom_path(redis_client, patient_list):
    """
    遍历患者集合，匹配对应DICOM路径
    :param patient_list
    :return new_patient_list [[patient_id,dicom_path]...]  or [[patient_id,[dicom_path,...]]...]
    """
    new_patient_list = []
    for patient in patient_list:
        patient_id = patient[0]
        if not redis_client.exists(patient_id):
            dicompath = select_pacs_exam_path_per_id(patient_id)  #   [[],[],[]....]
            dicompath = [i[0] for i in dicompath]
            #print dicompath
            count_path = str(len(dicompath))
            new_patient_list.append([patient_id, dicompath, count_path])
    return new_patient_list
#-----------------------------------------------------------------------------------------------------

def main(redis_client, channel,TEST):
    try:
        patient_list = select_id_list_from_study_status(TEST)  #  [patientid,body,exam_item,patient_source,modality,status]
        patient_list = get_patient_dicom_path(redis_client, patient_list) # 
        out("current patient number {}".format(len(patient_list)))

        if len(patient_list) > 0:
            Multi(redis_client, channel, patient_list,TEST) #start
    except:
        out("main run error")
        err(traceback.print_exc())

if __name__ == '__main__':
    mkdir_recursive('./log')

    try:
        rcon = redis.Redis()
        channel = "CT"
        channelCount = 1
        """
        receive 接收预测服务返回
        """
        if False:
            res_channel = "prediction"
            receive_analysis_response(rcon, res_channel) #更新预测结果到数据库
            out("receive predict server run start , channel : {}".format(res_channel))

        while True:
            out("server run start !")
            q = JoinableQueue()
            main(rcon, channel,TEST=False)  # 测试两分钟无误后修改为False
            time.sleep(float(config_obj.OTHER.server_sleep.value))
    except:
        out("run error")
        out(traceback.print_exc())
