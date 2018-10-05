# 推想假阳漏诊反馈脚本使用说明

假阳漏诊反馈脚本用于获取医生所反馈的相关图像。通过连入mongodb，获取TX_feedback/TX_falsePositive列表，读取PID & StudyId并将对应文件从源路径拷入目标路径。

## 配置config.py文件

config.py中定义了八个环境变量，分别为database,collection,source,destination,host,port  collection_1 destination_1 。
其中：
database & collection和collection_1为mongodb中对应的db和collection名称；
  - 主要修改collection和collection_1：TX_feedback/TX_falsePositive 分别对应 漏诊反馈/假阳反馈

source & destination和destination_1 分别为源路径及漏诊反馈和假阳目标路径的绝对路径；
  - 脚本会尝试从dicom的存储  源路径 source，拷贝到给定的指定路径 destination。

host & port为mongodb登录相关信息。

## 运行fpcheck.py

配置完成后直接运行
```
$ python fpcheck.py
```

## 测试

运行脚本后在目标路径内查看是否成功拷入相关图像即可。如有图像缺失，可在fpcheck.py的存放路径下查看filemissing.log。

## 版本

0.0.2



