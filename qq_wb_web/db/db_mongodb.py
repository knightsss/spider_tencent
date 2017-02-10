#coding=utf-8
__author__ = 'shifeixiang'
#连接数据库
import redis
from pymongo import *
#连接rtx
from log.rtx import rtx

#连接mongodb
def connect_mongodb():
    #新版本连接方式
    try:
        conn = MongoClient("192.168.15.111", 27017)
    except:
        conn = 0
        rtx('IP','mongodb连接异常')
    #旧版本连接方式
    # conn = pymongo.Connection("192.168.15.111",27017)
    return conn

#插入到qzone_info  monogo数据库
def load_mongodb_qzone_info(conn,qq,info):
    db = conn.db_tx_qzone_info
    t_tencent_qzone_info = db.t_tencent_qzone_info
    msg_label = {
        'qq':qq,
        'info':info
    }
    t_tencent_qzone_info.insert(msg_label)
    return 0