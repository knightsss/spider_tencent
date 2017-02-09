#coding=utf-8
__author__ = 'shifeixiang'
import time
import thread
import threading
from login.views import qzone_login
from db.db_redis import redis_connect,pop_redis_list,push_redis_list_tmp
from db.db_mysql import mysql_connect_qq,mysql_connect_local_qq,insert_mysql_qq,get_tuple

#import BeautifulSoup
from bs4 import BeautifulSoup
#加载异常处理
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from qzone_friend.models import Thread_qq_friend
from log.rtx import rtx,get_ip



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
    print "run......"
    driver = qzone_login()
    time.sleep(3)

    if driver == None :
        "phantomjs error!quit"
        return 0
    else:
        pass

    #连接redis
    conn_redis = redis_connect()
    redis_list_name_pop = "tencent_qzone_qq_test"
    redis_list_name_push = "tencent_qzone_qq_tmp_test"
    print "conn_redis",conn_redis
    if conn_redis == None  :
        print "redis connect error"
    else:
        ip = get_ip()
        while not c_thread.thread_stop:
            print 'qzone_qq_friend Thread:(%s) Time:%s\n'%(thread_num,time.ctime())
            qq = pop_redis_list(conn_redis,redis_list_name_pop)
            if qq == None:
                print "queue is NULL"
                break
            else:
                url = "http://user.qzone.qq.com/" + qq + "/mood"
                print "url",url
                driver.get(url)
                try:
                    #等待页面加载完成
                    frame_element = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "app_canvas_frame")))
                    print "find frame id"
                    driver.switch_to.frame('app_canvas_frame')
                    try:
                        #等待切换后的元素存在
                        class_name_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME , "comments_content")))
                        print "find conment"
                        html = driver.page_source
                        soup  = BeautifulSoup(html)
                        print "======"
                        my_set = set()
                        for i in soup.find_all(class_='comments_content'):
                            friend_qq = str(i.find('a')['href'])[25:-6]
                            print friend_qq
                            if friend_qq != qq:
                                my_set.add(friend_qq)
                        print my_set
                        friend_qq_list = list(my_set)
                        print friend_qq_list
                    except:
                        print "not found conment"
                        friend_qq_list = ['0']
                except:
                    print "没有权限访问"
                    friend_qq_list = ['-1']

                print friend_qq_list
                #############################################存入mysql
                try:
                    print "insert mysql"
                    #获取qq和friend_qq组成的元组，多个
                    tmp_tuple = get_tuple(qq,friend_qq_list)
                    #插入mysql数据库
                    print "insert into table "
                    mysql_conn = mysql_connect_qq()
                    insert_mysql_qq(mysql_conn,tmp_tuple)
                    #关闭数据库
                    mysql_conn.close()
                except:
                    rtx('ip',ip+ "机器QQ空间关系链采集mysql出错")
                ############################################存入临时的redis
                try:
                    print "put mid redis"
                    push_redis_list_tmp(conn_redis,redis_list_name_push,qq)
                    print "put auditor mid redis"
                    for friend_qq in friend_qq_list:
                        push_redis_list_tmp(conn_redis,redis_list_name_push,friend_qq)
                except:
                    rtx('ip',ip+ "机器QQ空间关系链采集redis入队出错")
        print thread_num,"quit phantomjs"
        driver.quit()
        #rtx提醒
        rtx('ip',ip+ "机器" + thread_num +"停止运行")
        #数据库状态更新,根据线程名称
        print "更新数据库线程状态"
        thread = Thread_qq_friend.objects.get(thread_name=thread_num)
        thread.thread_status = 0
        thread.save()


