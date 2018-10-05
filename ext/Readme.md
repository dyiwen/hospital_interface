# Monitor.py

用于向用户显示相应uid对应进程的cpu和gpu使用情况，目前仅针对dlserver测试。

## 前提

通常来说，在已有基础上，还需要psutil和gputil两个pip包，

    sudo pip install psutil；
    sudo pip install gputil

此外还需要在dlserver.py中，redis初始化后(rs = redis.StrictRedis(...))，加入以下两行代码：

    pid = os.getpid()
    rs.set('pid_to_monitor',pid)

需要先添加上述代码后，启动dlserver，然后再开始使用。

## 使用方式

python Monitor.py [time] 

>time 为时间间隔，每隔time秒输出一次当前使用情况日志，推荐使用 >[outpath]/monitor.log 方式输出日志方便查看检索



## 其他说明

该脚本目的为监控某个进程的使用情况，实际只需要在脚本的相应位置，对pid的获取进行更改，就可以对某个你想要监控的进程进行监视。具体使用方法请灵活调整！
