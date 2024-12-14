import pytz
import time
import datetime


def nowtime():
    cn = pytz.timezone('Asia/Shanghai')
    cn_time = datetime.datetime.now(cn).strftime("%Y-%m-%d %H:%M:%S")
    local_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return cn_time, local_time


def log_write(log):
    thetime = nowtime()
    with open('./log/log.txt', encoding='utf-8', mode='a') as files:
        files.write("[{}] {}\n".format(thetime[0], log))
        files.close()


def bug_write(bug):
    thetime = nowtime()
    with open('./log/bug.txt', encoding='utf-8', mode='a') as files:
        files.write("[{}] {}\n".format(thetime[0], bug))
        files.close()


def admin_write(admin):
    thetime = nowtime()
    with open('./log/admin.txt', encoding='utf-8', mode='a') as files:
        files.write("[{}] {}\n".format(thetime[0], admin))
        files.close()
