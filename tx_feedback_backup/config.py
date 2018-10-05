# -*- coding: utf-8 -*-
class config(object):pass

class TXDB(object):pass

#txdb
config.TXDB = TXDB()
config.TXDB.user = "root"    #数据库用户名
config.TXDB.pwd = "root"     #数据库密码
config.TXDB.ip = "127.0.0.1"    #数据库地址
config.TXDB.port = "3306"    #数据库端口
config.TXDB.database = "txdata"    #数据库名称


class PATH(object):pass
#feedbackpath
config.PATH = PATH()
config.PATH.dicom_path = "/media/tx-deepocean/Data/DICOMS/CT/"    #需要备份的dicom路径
config.PATH.output_path = "/media/tx-deepocean/Data/output/CT/"    #需要备份的预测结果文件夹路径
config.PATH.feedback_path = "/media/tx-deepocean/Data/feedback_backup/"    #备份输出文件夹路径



