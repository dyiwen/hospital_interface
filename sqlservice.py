#!/usr/bin/env python
# encoding: utf-8

from tools.DB import DAL
import numpy as np
import os,json
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'


def show_chinese(data):
    show_china = json.dumps(data,encoding = 'UTF-8',ensure_ascii = False)
    return show_china
#---------------------------------------------------------------------------------------------------------


def select_pacs_exam_path_per_id(patient_id):
    """
    医院pacs:获取指定pid 影像
    :param patient_id: 影像号
    :return: path 影像路径

    """ 
    orc = DAL.Oracle("user", "pwd", "host", port, "ORCL")
    sql = "select distinct unc_path from VIEW_NAME where accessionno = '{}' and exam_date_time >= trunc(sysdate)\
    and REGEXP_LIKE(body,'胸部|腹部') and REGEXP_LIKE(exam_item,'胸|上腹部') and modality like 'CT' and REGEXP_LIKE(status,'上传图像完成|诊断完成|暂存')".format(patient_id)
    rowcount,result = orc.execute(sql)
    orc.close()
    #print result
    return result

#---------------------------------------------------------------------------------------------------------------------------------------------------------

def select_id_list_from_study_status(TEST):
    """
    医院ris:获取已检查但医生未写报告的病人
    :return: patient 病人基本信息 type list
    """
    if TEST:
        return [[str(i), ""] for i in np.random.randint(10000000, 99999999, 10)]
    #--------------------------------------------------------------------------------------------------
    orc = DAL.Oracle("user", "pwd", "host", port, "ORCL")    
    sql = "select distinct accessionno,exam_item,patient_source,modality,status from VIEW_NAME where exam_date_time >= trunc(sysdate) \
    and REGEXP_LIKE(body,'胸部|腹部') and REGEXP_LIKE(exam_item,'胸|上腹部') and modality like 'CT' and REGEXP_LIKE(status,'上传图像完成|诊断完成|暂存')"
    rowcount,result = orc.execute(sql)
    orc.close()
    # print show_chinese(result)
    # print 'total num is :',len(result)
    return result


if __name__ == '__main__':
    select_id_list_from_study_status(False)
    #select_pacs_exam_path_per_id('20180817000895')
