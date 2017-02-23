#coding=utf-8
from django.shortcuts import render

# Create your views here.
from selenium import webdriver
import time
from log.rtx import rtx
from tencent_wb_user.models import TencentUser
from tencent_wb_user.models import TencentProxy
import random
import base64

def qzone_login():

    USER_COUNT = TencentUser.objects.count()
    PROXY_COUNT = TencentProxy.objects.count()

    user_number = random.randint(1, USER_COUNT)

    #去数据库中取，随机获取登陆帐号
    user = TencentUser.objects.get(user_id=user_number)
    login_name = user.login_name
    #密码解密s2 = base64.decodestring(s1)
    login_pwd = base64.decodestring(user.login_password)
    qq_qzone_name = user.qq_qzone_name

    login_flag = 1
    login_times = 1
    while login_flag:
        driver_flag = 1
        driver_times = 1
        while driver_flag:
            try:
                #driver = webdriver.PhantomJS('E:\\phantomjs\\phantomjs-2.1.1-windows\\phantomjs-2.1.1-windows\\bin\\phantomjs')
                driver = webdriver.PhantomJS(executable_path='/usr/local/phantomjs/bin/phantomjs',service_log_path='/data/tmp/ghostdriver.log')
                driver_flag = 0
            except:
                print "PhantomJS error,wait a moment!"
                time.sleep(10)
            driver_times = driver_times + 1
            if driver_times > 5:
                driver_flag = 0

        try:
            driver.get("http://i.qq.com/")
            time.sleep(3)
            # driver.switch_to_frame("login_frame")
            driver.switch_to.frame("login_frame")
            driver.find_element_by_id("switcher_plogin").click()
            driver.find_element_by_id("u").send_keys(login_name)
            driver.find_element_by_id("p").send_keys(login_pwd)
            driver.find_element_by_id("login_button").click()
            time.sleep(10)
            print "driver.current_url is",driver.current_url
            print "match is : ","http://user.qzone.qq.com/" + str(qq_qzone_name)
            if driver.current_url == "http://user.qzone.qq.com/" + str(qq_qzone_name) or driver.current_url == "https://user.qzone.qq.com/" + str(qq_qzone_name) :
                login_flag = 0
            else:
                print "url 不一致!"
                driver.quit()
        except:
            print "login error!"
            driver.quit()

        login_times = login_times + 1
        if login_times > 10:
            rtx('ip','qq login error')
            driver = None
            login_flag = 0
    return driver
