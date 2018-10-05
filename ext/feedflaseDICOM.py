#!/usr/bin/python
# -*- coding: utf-8 -*-
#JiaKeXin
#按时间最早在前的顺序排列出目录文件
import os, time ,sys
import shutil

DIR = "/media/tx-deepocean/Data/feedback"
#将两个“>和<”的顺序调换可以实现升降序的调换。
def compare(x, y):
    stat_x = os.stat(DIR + "/" + x)
    stat_y = os.stat(DIR + "/" + y)
    if stat_x.st_ctime < stat_y.st_ctime:
        return -1
    elif stat_x.st_ctime > stat_y.st_ctime:
        return 1
    else:
        return 0
 
iterms = os.listdir(DIR)
 
iterms.sort(compare)
 
for iterm in iterms:
    print iterm

#print disk user_data
last_worktime=0
last_idletime=0

def usage_percent(use, total):
    try:
        ret = (float(use) / total) * 100
    except ZeroDivisionError:
        raise Exception("ERROR - zero division error")
    return ret
#修改不同文件目录可以查看不同的空间使用率
statvfs = os.statvfs('/media/tx-deepocean/Data')

total_disk_space = statvfs.f_frsize * statvfs.f_blocks
free_disk_space = statvfs.f_frsize * statvfs.f_bfree
disk_usage = (total_disk_space - free_disk_space) * 100.0 / total_disk_space
disk_usage = int(disk_usage)
disk_tip = "硬盘空间使用率（最大100%）："+str(disk_usage)+"%"
print (disk_tip)
#delete floder
pointer = len(iterms)-1
while disk_usage > 90 and pointer >= 0:
    print(iterms[pointer])
#添加删除图片路径。
    shutil.rmtree(os.path.join("/media/tx-deepocean/Data/feedback", iterms[pointer]))
    pointer -= 1
    statvfs = os.statvfs('/media/tx-deepocean/Data')
    total_disk_space = statvfs.f_frsize * statvfs.f_blocks
    free_disk_space = statvfs.f_frsize * statvfs.f_bfree
    disk_usage = (total_disk_space - free_disk_space) * 100.0 / total_disk_space
    print("{}%".format(disk_usage))
