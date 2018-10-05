数据拉取-接口（对接医院）
===
 * tools/ 工具集合
 * reset.py 重置/生成配置文件（./server.conf）
 * server.py 服务启动 
 * constants.py 公共常量
 * sqlserver.py sql管理
 * pulldata.py 获取DICOM
 * ext/ 附加的功能


* 重置/生成配置文件

```
$ python reset.py
```
* 启动

```
$ python multi_server.py
```     

* 测试   
默认会执行多轮测试，输出的每一轮运行时间等于30/cpuCount*10则多进程没有问题    
测试无误后需要修改：    
    TEST=True改为False    


常修改地方（注意地方）
* multi_server.py  
    * function: service()
        * 选择合适获取DICOM文件的方式 或 本地编写function；
        * file_number 设置预测最小文件个数；
        * 该脚本的过滤函数添加至了pulldata.py
    * function: main() 
        * 对数据库的查询信息进行数据清洗 
    * function: Multi() 
        * cpuCount= 根据CPU的核数分配进程（通过CPUCOUNT()计算），一般最大为12,可根据显示情况写死       
    * channelCount 对应多通道的DLSERVER
   
* dcmlib 脱敏包，对图像的处理图像敏感信息
* log 日志管理目录，在此追踪脚本日常运行
* sqlserver.py 根据医院数据库结构本地编写SQL，封装的SQL类位于DAL，支持sqlserver,mysql,oracle     
* server.conf  一些常用参数可以在此修改    
* constants.py  根据日志级别分别封装,取消注释out函数中的print用于观察     
 
