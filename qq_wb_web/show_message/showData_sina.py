#-*- coding:utf-8 -*-
'''
Created on 2017年4月7日

@author: huangjiaxin
'''
import pymongo
import json
import copy
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def catchDetail(cursor):
    messageLists = []
    for document in cursor:
        #the item of message
        messageDict = dict()
        #fill the message
        messageDict['id'] = document['_id']
        messageDict['city'] = document['city']
        messageDict['messageCount'] = document['messageCount']
        messageDict['level'] = document['level']
        messageDict['UserId'] =document['UserId']
        messageDict['follower'] = document['follower']
        messageDict['summary'] = document['summary']
        messageDict['user_work'] = document['user_work']
        messageDict['following'] = document['following']
        messageDict['user_name'] = document['user_name']
        #change the talkList
        for k in document['talkList']:
            tempDict = messageDict
            for key, cont in document['talkList'][k].items():
                tempDict[key] = cont
            messageLists.append(copy.deepcopy(tempDict))
    return messageLists


def txwbshow(db_name, tablename, num=10):
    '''
              固定信息的key：
        id
        city
        messageCount
        level
        UserId
        follower
        summary
        user_work
        following
        user_name
        tran_content
        msg_content
        date_time
        picturl_or_vedio
        platform
    '''
    client = pymongo.MongoClient("192.168.8.25", 27017)
    try:
        database = client[db_name]
        table = database[tablename]
        cursor = table.find().limit(num)
        messageLists = catchDetail(cursor)
        return messageLists
    except Exception, e:
        print e
    finally:
        client.close()
        

def getsinawbDetail(cursor):
    messageLists = []
    for document in cursor:
        messageLists.append(document)
    return messageLists

      
def sinawbshow(db_name, tablename, num=10):
    '''
    因为存储格式的便利，所以不用再增加处理函数。
    _id
    person_href
    person_name
    labels
    sex
    personInfo
    personNum
    addString
    '''
    client = pymongo.MongoClient("192.168.8.25", 27017)
    try:
        database = client[db_name]
        table = database[tablename]
        cursor = table.find().limit(num)
        messageLists = getsinawbDetail(cursor)
        return messageLists
    except Exception, e:
        print e
    finally:
        client.close()


def getshuoshuoDetail(cursor):
    tempList = []
    for document in cursor:
        messageDict = dict()
        messageDict['id'] = document['_id']
        messageDict['number'] = document['number:']
        #删除不便于处理的key值
        del document['_id']
        del document['number:']
        del document['can_load']
        
        for key, content in document.items():
            tempDict = messageDict
            for key_c, val_c in content.items():
                tempDict[key_c] = val_c
            tempList.append(copy.deepcopy(tempDict))
    return tempList


def shuoshuoshow(db_name, table_name, num=10):
    '''
    id
    number
    content
    date_and_platform
    op_of_reader
    rt_contents
    mood_comments_list
    '''
    client = pymongo.MongoClient("192.168.8.25", 27017)
    try:
        database = client[db_name]
        table = database[table_name]
        cursor = table.find().limit(num)
        messageLists = getshuoshuoDetail(cursor)
        return messageLists
    except Exception, e:
        print Exception, e
    finally:
        client.close()


if __name__ == '__main__':
    print shuoshuoshow('db_shuoshuo_content', 't_shuoshuo_content', 2)
    print sinawbshow('db_sina_wb', 't_youxi_labels', 2)
    print txwbshow('db_tx_wb_content', 't_weibo_content', num=2)
    pass