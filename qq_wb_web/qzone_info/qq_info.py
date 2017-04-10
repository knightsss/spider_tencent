#coding=utf-8
__author__ = 'shifeixiang'

from login.login import qzone_login
import time
from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_info(driver, url, log):
        try:
            # print "url is : ",url
            driver.set_page_load_timeout(30)
            driver.get(url)     #获取网址异常判断
        except:
            print "20s timeout! againt visit!"
            try :
                driver.set_page_load_timeout(15)
                driver.get(url)     #获取网址异常判断
            except:
                #将未加载完成的qq写入文件
                log.info("request error!!!")
                print "Timeout! quit current page right now!"
                driver.quit()
                # driver = qzone_login()
                return 0
        #捕获空间访问异常的情况
        try:
            driver.find_element_by_id('aOwnerFeeds').click()        #是否具有访问权限，有的话，
            time.sleep(3)
        except:
            #将未加载完成的qq写入文件
            log.info("Refuse visit!!!")
            return 1
        time.sleep(3)
        try:
            driver.find_element_by_class_name('head-detail-name').text
        except:
            log.info("get name error!")
            #考虑将名字未找到的qq写入文件
            log.info("Timeout! quit current page right now!")
            return 1
            # name = "None"
        try:
            driver.find_element_by_class_name('detail-info-level')          #黄钻是否存在
            diamon = "黄钻"
            try:
                driver.find_element_by_class_name('detail-info-con')
                value = driver.find_element_by_class_name('txt-value').text     #成长值
                speed = driver.find_element_by_class_name('txt-speed').text     #成长速度
            except:
                value = "None"
                speed = "None"
        except:
            diamon = "None"
            value = "None"
            speed = "None"
        #捕获获取个人信息异常的情况
        try:
            driver.switch_to.frame(driver.find_element_by_class_name('app_canvas_frame'))   #切换到对应的子框架
            time.sleep(5)
            try:
                element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID , "info_tab")))
                print "个人信息可获取"
            except:
                print "未发现u_info，网络加载较慢"
            #获取个人信息
            print "获取个人信息!"
            # time.sleep(5)
            driver.find_element_by_id('info_tab').click()
            time.sleep(5)
            my_page = driver.page_source
            soup = BeautifulSoup(my_page)

            name_element = soup.find(id="nickname_n")
            for name_sub in name_element.stripped_strings:
                name = name_sub
            sex_element = soup.find('div',id="sex")
            for sex_sub in sex_element.stripped_strings:
                sex = sex_sub

            age_element = soup.find('div',id="age")
            for age_sub in age_element.stripped_strings:
                age = age_sub

            birthday_element = soup.find('div',id="birthday")
            for birthday_sub in birthday_element.stripped_strings:
                birthday = birthday_sub

            astro_element = soup.find('div',id="astro")
            for astro_sub in astro_element.stripped_strings:
                astro = astro_sub

            live_address = ""
            live_address_element = soup.find('div',id="live_address")
            for live_address_sub in live_address_element.stripped_strings:
                live_address = live_address + live_address_sub

            marriage_element = soup.find('div',id="marriage")
            for marriage_sub in marriage_element.stripped_strings:
                marriage = marriage_sub

            blood_element = soup.find('div',id="blood")
            for blood_sub in blood_element.stripped_strings:
                blood = blood_sub

            hometown_address = ""
            hometown_address_element = soup.find('div',id="hometown_address")
            for hometown_address_sub in hometown_address_element.stripped_strings:
                hometown_address = hometown_address + hometown_address_sub

            career_element = soup.find('div',id="career")
            for career_sub in career_element.stripped_strings:
                career = career_sub

            company_element = soup.find('div',id="company")
            for company_sub in company_element.stripped_strings:
                company = company_sub

            company_caddress = ""
            company_caddress_element = soup.find('div',id="company_caddress")
            for company_caddress_sub in company_caddress_element.stripped_strings:
                company_caddress = company_caddress + company_caddress_sub

            caddress_element = soup.find('div',id="caddress")
            for caddress_sub in caddress_element.stripped_strings:
                caddress = caddress_sub
            time.sleep(3)
            info_list = []
            # info_list.append(qq)
            info_list.append(name.encode('utf-8'))
            info_list.append(diamon)
            info_list.append(value.encode('utf-8'))
            info_list.append(speed.encode('utf-8'))
            try:
                info_list.append(sex)
            except:
                info_list.append("未填写")
            info_list.append(age)
            info_list.append(birthday.encode('utf-8'))
            info_list.append(astro.encode('utf-8'))
            #8
            info_list.append(live_address.encode('utf-8'))
            info_list.append(marriage.encode('utf-8'))
            info_list.append(blood.encode('utf-8'))
            info_list.append(hometown_address.encode('utf-8'))
            info_list.append(career.encode('utf-8'))
            info_list.append(company.encode('utf-8'))
            info_list.append(company_caddress.encode('utf-8'))
            info_list.append(caddress.encode('utf-8'))
        except:
            log.info("get msg error!")
            return 1
        return info_list
