#coding=utf-8
__author__ = 'shifeixiang'
import time
import thread
import threading

from log.views import log_setting
from log.rtx import rtx,get_ip
#登陆
from login.login import qzone_login
#数据库
from db.db_redis import redis_connect,pop_redis_list,push_redis_list_tmp
from db.db_mongodb import connect_mongodb,load_mongodb_qzone_info
#info
from qzone_info.qq_info import get_info
#模式
from qzone_info.models import ThreadQzoneInfo

class Spider(threading.Thread):
    # __metaclass__ = Singleton
    thread_stop = False
    thread_num = 0
    interval = 0
    behavior = None
    def run(self):
        self.behavior(self,self.thread_num,self.interval)
    def stop(self):
        self.thread_stop = True

class ThreadControl():
    thread_stop = False
    current_thread = {}
    def start(self,thread_num,interval):
        spider = Spider()
        spider.behavior = loaddata
        spider.thread_num = thread_num
        spider.interval = interval
        spider.start()
        self.current_thread[str(thread_num)] = spider
    #判断进程是否活跃
    def is_alive(self,thread_num):
        tt = self.current_thread[str(thread_num)]
        return tt.isAlive()
    #获取当前线程名称
    # def get_name(self):
    def stop(self,thread_num):
        print "stop"
        spider = self.current_thread[str(thread_num)]
        spider.stop()

def loaddata(c_thread,thread_num,interval):
    print thread_num,"run......"
    driver = qzone_login()
    time.sleep(3)

    if driver == None :
        "phantomjs error!quit"
        return 0
    else:
        pass
    #出队
    conn_redis = redis_connect()
    conn_mongo = connect_mongodb()
    print "conn_redis",conn_redis
    print "conn_mongo",conn_mongo
    #定义pop的redis名字
    redis_list_pop_name = "tencent_qzone_qq_info_tmp"
    redis_list_push_qzone_forbid_name = "tencent_qzone_forbid_qq_tmp"

    if conn_redis == 0 or conn_mongo == 0:
        print "redis or mongodb connect error"
    else:
        ip = get_ip()
        while not c_thread.thread_stop:
            print 'Thread:(%s) Time:%s\n'%(thread_num,time.ctime())
            log = log_setting()
            log.info('Thread:(%s) Time:%s\n'%(thread_num,time.ctime()))
            #pop_redis_list(redis_conn,redis_list_name)
            qq = pop_redis_list(conn_redis,redis_list_pop_name)
            #判断队列是否为空
            if qq == None:
                print "queue is NULL"
                break
            else:
                #获取详细信息
                url = "http://user.qzone.qq.com/"+str(qq)+"/profile"
                info_list = get_info(driver,url)
                # msg = get_msg(driver,url)
                if info_list == 0:
                    #qq放入redis消息队列
                    push_redis_list_tmp(conn_redis,redis_list_push_qzone_forbid_name,qq)
                    pass
                else:
                    #存入mongodb
                    print "load to mongodb"
                    try:
                        load_mongodb_qzone_info(conn_mongo,qq,info_list)
                    except:
                        rtx('ip',ip+ "机器mongodb失败")
                        print "mongodb error"
                        break
        # rtx('IP','正常停止')
        print thread_num,"quit phantomjs"
        driver.quit()
        #rtx提醒
        rtx('ip',ip+ "机器" + thread_num +"停止运行")
        #数据库状态更新,根据线程名称
        print "更新数据库线程状态"
        thread = ThreadQzoneInfo.objects.get(thread_name=thread_num)
        thread.thread_status = 0
        thread.save()

