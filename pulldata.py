#!/usr/bin/env python
# encoding: utf-8

import sys, os, time, traceback, shutil

import subprocess
from subprocess import CalledProcessError
from tools.RSYNC.FTP_ import FTPrsync, RsyncExtra
from tools.SYSTEM.threading_ import pooled

import zipfile
from constants import config, config_obj, out, err, exception, warn
import dicom

from sqlservice_test import sql_test




def unzip(source):
    """
    解压提取
    :param source: 文件路径
    :return:
    """
    try:
        with zipfile.ZipFile(source, "r") as zf:
            zf.extractall()
            zf.close()
    except:
        out("解压失败 {}".format(source))
        err(traceback.format_exc())

def gdcmconv(source):
    """
    gdcm 解压dicom文件
    :param source: 数据源，dicom目录
    """
    for rootpath, folder, filenames in os.walk(source):
        for filename in filenames:
            filepath = os.path.join(rootpath, filename)
            cmd = "gdcmconv -w {} {}".format(filepath, filepath)
            os.system(cmd)

#------------------------------------------------------------------------------
def isnotdicom(s):
    try:
        ds = dicom.read_file(s)
    except:
        try:          
            os.remove(s)
        except:
            out('没有该路径 {}'.format(s))
            warn(traceback.format_exc())
        return True

def isnotslice(s):
    try:
        ds = dicom.read_file(s)
        ds.SliceThickness
    except:
        os.remove(s)
        return True

def filter_slice(destination):
    for roots,dirs,files in os.walk(destination):
        for file_ in files:
            a = os.path.join(roots,file_)
            if not isnotdicom(a):
                ds = dicom.read_file(a)
                try:
                    if not isnotslice(a) and ds.SliceThickness not in [0.625000,1,1.25000,1.5]:
                        os.remove(a)
                except:
                    print "Don't have SliceThickness"
                    os.remove(os.path.join(roots,file_))

def filter_sop(destination):
    SOP_list = []
    for roots,dirs,files in os.walk(destination):
        for sop_path in files:
            print sop_path
            remove_path = os.path.join(roots,sop_path)
            try:
                ds = dicom.read_file(remove_path)
                #print ds.SOPInstanceUID
                remove_parts =  int(ds.SOPInstanceUID.split('.')[-2])
                if remove_parts not in SOP_list:
                    SOP_list.append(remove_parts)
            except: 
                print "Don't have SOPInstanceUID"
                traceback.print_exc()
                os.remove(remove_path)
    print SOP_list
    for remove_UID in files:
        remove_UID_path = os.path.join(roots,remove_UID)
        ds2 = dicom.read_file(remove_UID_path)
        if int(ds2.SOPInstanceUID.split('.')[-2]) != min(SOP_list):
            os.remove(remove_UID_path)

def filter_dicom(destination):
    filter_slice(destination)
    filter_sop(destination)
#------------------------------------------------------------------------------------

def ftp_download(obj, source, destination):         #config_obj.FTP, dicompath, outpath
    """
    下载文件
    :param source: FTP文件路径
    :param destination: dicom存储路径
    :return: dicom个数
    """
    try:
        ftpsync = RsyncExtra(user=obj.username.value, pwd=obj.password.value, host=obj.host.value,
                             port=obj.port.value, timeout= 60)
        #ftpsync.func = unzip
        out('开始下载 {}'.format(os.path.split(destination)[1]))
        ftpsync.sync(source, destination,tree= False)
        out('下载解压删除完毕 {}'.format(os.path.split(destination)[1]))
        filter_dicom(destination)
        out('过滤完毕 {}'.format(os.path.split(destination)[1]))
    except:
        out("ftp下载病人影像失败 {}".format(source[0]))
        err(traceback.format_exc())
    return len(os.listdir(destination))


if __name__ == '__main__':
    # filter_slice('/media/tx-deepocean/Data/DICOMS/20180819000045')
    #filter_dicom('/media/tx-deepocean/Data/DICOMS/20180819000045')
    # isnotdicom('/home/tx-deepocean/Downloads/testt.py')


    a = sql_test()
    a = [i[0] for i in a]
    print a
    ftp_download(config_obj.FTP,a,'/media/tx-deepocean/Data/DICOMS/20180819000045')
