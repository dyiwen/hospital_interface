#!/bin/bash
cd /home/tx-deepocean/Infervision/tx_feedback_backup
mysql_ready() {
        mysqladmin ping --user=tuixiang --password=tuixiang > /dev/null 2>&1
    }
while !(mysql_ready)
do
   sleep 3
   echo "waiting for mysql ..."
done
python ./feedback_backup.py