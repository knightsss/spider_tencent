# coding=utf-8
__author__ = 'shifeixiang'
import redis
from log.rtx import rtx

def redis_connect():
    #带密码连接
    # r = redis.StrictRedis(host='localhost', port=6379, password='npq8pprjxnppn477xssn')
    try:
        redis_conn = redis.Redis(host='192.168.8.25',port=6379,db=0)
    except:
        rtx('IP','redis连接异常')
        print "connect redis error"
        redis_conn = 0
    return redis_conn

#出wid消息队列
###redis连接 redis list名字
def pop_redis_list(redis_conn,redis_list_name):
    try:
        qq = redis_conn.lpop(redis_list_name)
        # print "pop ok"
    except:
        # redis_conn = redis_connect()
        print "pop faild"
        qq = None
    return qq

# #入临时消息队列
###redis连接 redis list名字 value
def push_redis_list_tmp(redis_conn,redis_list_name,value):
    try:
        redis_conn.rpush(redis_list_name,value)
    except:
        redis_conn = redis_connect()