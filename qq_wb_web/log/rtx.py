#coding=utf-8
__author__ = 'shifeixiang'
import time
import os
import urllib2
import base64
import hashlib
import sys
#from hdfs.client import Client
import logging
import logging.config
import socket


import socket
#fcntl是posix接口，windows下没有的
# import fcntl
import struct
#禁止使用
'''
def get_ip():
    IP = socket.gethostbyname(socket.gethostname())
    return IP
'''
#通过网卡获取
def get_ip():
    ifname = "eth0"
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


def rtx(base_title,base_msg):
    # msg_db = sys.argv[1]
    # msg_tab = sys.argv[2]
    #msg_file = sys.argv[3]
    IP = get_ip()
    base_title = base_title + IP
    title = base64.b64encode(base64.b64encode(base_title))
    receiver_list = []
    receiver_list.append('shifeixiang')
    for receiver in receiver_list:
        msg = base64.b64encode(base64.b64encode(base_msg))
        receiver = str(receiver)
        stamp = str(int(time.time()))

        sign_tmp = receiver + base_msg + stamp + 'MINGCHAO::API::RTX::4YHb&fovu^!6Kjh'

        hash_md5  = hashlib.md5(sign_tmp)
        sign = hash_md5.hexdigest()
        sign = sign.upper()

        url = 'http://call.mingchaoonline.com/rtx/mc_api_rtx_notice.php?' + 'title=' + title + \
              '&msg=' + msg +  \
              '&receiver=' + receiver + \
              '&stamp=' + stamp + \
              '&sign=' + sign

        result = urllib2.urlopen(url)
        res = result.read()
        print res
