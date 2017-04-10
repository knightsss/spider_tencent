#-*- coding:utf-8 -*-
'''
Created on 2017年4月7日

@author: huangjiaxin
'''
import pymongo
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def catchdetail(document, messageLists):
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
        messageLists.append(tempDict)
    return messageLists


def txwbshow(db_name, tablename, num=2):
    client = pymongo.MongoClient("192.168.8.25", 27017)
    try:
        database = client[db_name]
        table = database[tablename]
        cursor = table.find().limit(num)
        messageLists = []
        for document in cursor:
            messageLists = catchdetail(document, messageLists)
        return messageLists
    except Exception, e:
        print e
    finally:
        client.close()
        

if __name__ == '__main__':
    print txwbshow('db_tx_wb_content', 't_weibo_content', num=10)