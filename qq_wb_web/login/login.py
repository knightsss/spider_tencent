#coding=utf-8
from django.shortcuts import render

# Create your views here.
from selenium import webdriver
import time
from log.rtx import rtx

def qzone_login():
    login_flag = 1
    login_times = 1
    while login_flag:
        flag = 1
        while flag:
            try:
                #driver = webdriver.PhantomJS('E:\\phantomjs\\phantomjs-2.1.1-windows\\phantomjs-2.1.1-windows\\bin\\phantomjs')
                driver = webdriver.PhantomJS(executable_path='/usr/local/phantomjs/bin/phantomjs',service_log_path='/data/tmp/ghostdriver.log')
                flag = 0
            except:
                print "PhantomJS error,wait a moment!"
                time.sleep(10)
        try:
            driver.get("http://i.qq.com/")
            time.sleep(3)
            # driver.switch_to_frame("login_frame")
            driver.switch_to.frame("login_frame")
            driver.find_element_by_id("switcher_plogin").click()
            driver.find_element_by_id("u").send_keys("2089634140@qq.com")
            driver.find_element_by_id("p").send_keys("mk123456789")
            driver.find_element_by_id("login_button").click()
            time.sleep(10)
            print "driver.current_url is",driver.current_url
            if driver.current_url == "http://user.qzone.qq.com/1251314160" :
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
            break
    return driver
