#coding=utf-8
from django.shortcuts import render

# Create your views here.
from selenium import webdriver
import time

def qzone_login():
    flag = 1
    while flag:
        try:
            #driver = webdriver.PhantomJS('E:\\phantomjs\\phantomjs-2.1.1-windows\\phantomjs-2.1.1-windows\\bin\\phantomjs')
            driver = webdriver.PhantomJS(executable_path='/usr/local/phantomjs/bin/phantomjs')
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
        driver.find_element_by_id("u").send_keys("1251314160@qq.com")
        driver.find_element_by_id("p").send_keys("sfx123plmoknijb")
        driver.find_element_by_id("login_button").click()
        time.sleep(10)
        print "driver.current_url is",driver.current_url
        if driver.current_url == "http://user.qzone.qq.com/1251314160" :
            pass
        else:
            print "url 不一致!"
            driver.quit()
            qzone_login()
    except:
        print "login error!"
        driver.quit()
        qzone_login()
    return driver
