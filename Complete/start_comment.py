#coding=utf8
import sys 
sys.path.append(r'C:\env')
import time

from Complete import jrtt_mongo_update , jrtt_comment_thread


work_time = "23:00:00"

while True:
    now_time = int(time.time())
    local_time = time.localtime(now_time)
    hours = time.strftime("%H:%M:%S", local_time)
    if hours != work_time:
        time.sleep(1)
        print("等待中",hours)
    else:
        jrtt_mongo_update.main()
        jrtt_comment_thread.main()
