# coding=utf-8
__author__ = 'shifeixiang'
import MySQLdb
from log.rtx import rtx

def mysql_connect_qq():
    try:
        mysql_conn = MySQLdb.connect("192.168.8.25","qzone_spider","qzone_spider","db_tencent_qzone")
    except:
        print "connect mysql error"
        rtx('IP','mysql连接异常')
        return None
    return mysql_conn

def mysql_connect_local_qq():
    try:
        mysql_conn = MySQLdb.connect("localhost","qzone_spider","qzone_spider","db_tencent_qzone")
    except:
        print "connect mysql error"
        rtx('IP','mysql连接异常')
        return None
    return mysql_conn

def insert_mysql_qq(mysql_conn,tmp):
    mysql_cursor = mysql_conn.cursor()
    sql = "insert into t_tencent_qzone_qq(qq, friend_qq) values(%s, %s)"
    # tmp结构 tmp = (('00', '0000'), ('10', '111'))
    mysql_cursor.executemany(sql, tmp)
    mysql_conn.commit()
    return 0

def get_tuple(mid,mid_list):
    tmp_list = []
    for auditor_url in mid_list:
        tmp_tup = (mid,auditor_url)
        tmp_list.append(tmp_tup)
    return tuple(tmp_list)