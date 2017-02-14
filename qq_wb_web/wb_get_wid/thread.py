#coding=utf-8
__author__ = 'shifeixiang'
import time
import thread
import threading
from wb_get_wid.auditor import redis_connect,pop_redis_list,get_auditor_page_url_via_url,get_auditor_main_url,mysql_connect,get_tuple,insert_mysql,push_redis_list_tmp
from qq_wb_msg.msg import qq_login

from log.rtx import rtx,get_ip
from wb_get_wid.models import Threadauditor
from log.views import log_setting

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
    log_name_title = "tencent_wb_auditor_"
    base_date = time.strftime("%Y%m%d", time.localtime())
    log = log_setting(log_name_title + base_date + ".log")
    log.info("run......")
    driver = qq_login()
    time.sleep(3)

    if driver == None :
        log.info("phantomjs error!quit")
        return 0
    else:
        pass

    #连接redis
    conn_redis = redis_connect()
    #mysql连接 异常返回None
    #mysql_conn = mysql_connect()
    # conn_mongo = connect_mongodb()
    log.info("conn_redis" + conn_redis)
    # print "conn_mongo",conn_mongo
    if conn_redis == None  :
        log.info("redis connect error")
    else:
        ip = get_ip()
        while not c_thread.thread_stop:
            current_date = time.strftime("%Y%m%d", time.localtime())
            if current_date == base_date:
                pass
            else:
                base_date = current_date
                log = log_setting(log_name_title + base_date + ".log")
            log.info('Thread:(%s) Time:%s'%(thread_num,time.ctime()))
            mid = pop_redis_list(conn_redis)
            if mid == None:
                log.info("queue is NULL")
                break
            else:

                url = "http://t.qq.com/" + str(mid)
                log.info("url is: " + url)
                time.sleep(3)
                #根据用户的主页url获取收听的所有页面
                auditor_page_url_list = get_auditor_page_url_via_url(driver,url)
                if auditor_page_url_list == None:
                    log.info("page is not personal,login again")
                    driver.quit()
                    driver = qq_login()
                    if driver == None:
                        break
                    else:
                        pass
                #根据收听的所有页面获取收听者的主页url
                ################根据已知mid获取所有收听的mid
                else:
                    mid_list = get_auditor_main_url(driver, auditor_page_url_list)
                    if mid_list == None:
                        continue
                    else:
                        #############################################存入mysql
                        try:
                            log.info("insert mysql")
                            #获取mid和auditor_mid组成的元组，多个
                            tmp_tuple = get_tuple(mid,mid_list)
                            #插入mysql数据库
                            print "insert into table "
                            mysql_conn = mysql_connect()
                            insert_mysql(mysql_conn,tmp_tuple)
                            #关闭数据库
                            mysql_conn.close()
                        except:
                            rtx('ip',ip+ "机器mysql出错")
                            log.info('ip'+ ip+ "机器mysql出错")
                            log.info("insert mysql error")
                        ############################################存入临时的redis
                        try:
                            log.info("put mid redis")
                            push_redis_list_tmp(conn_redis,mid)
                            log.info("put auditor mid redis")
                            for auditor_mid in mid_list:
                                push_redis_list_tmp(conn_redis,auditor_mid)
                        except:
                            rtx('ip',ip+ "机器redis出错")
                            log.info('ip' + ip + "机器redis出错")
                            log.info("insert redis error")

        log.info(thread_num + "quit phantomjs")
        driver.quit()
        #rtx提醒
        rtx('ip',ip+ "机器" + thread_num +"停止运行")
        log.info('ip'+ ip + "机器" + thread_num + "停止运行")
        #数据库状态更新,根据线程名称
        log.info("更新数据库线程状态")
        thread = Threadauditor.objects.get(thread_name=thread_num)
        thread.thread_status = 0
        thread.save()
        
