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


def catchdetail(document):
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
        talkList
    talkList内容中的key有：
        tran_content
        msg_content
        date_time
        picturl_or_vedio
        platform
    '''
    #the item of message
    id = dict()
    city = dict()
    messageCount = dict()
    level = dict()
    UserId = dict()
    follower = dict()
    summary = dict()
    user_work = dict()
    following = dict()
    user_name = dict()
    talkList = dict()
    
    messageLists = []
    messageList = []
    #fill the message
    id['id'] = document['_id']
    messageList.append(id)
    city['city'] = document['city']
    messageList.append(city)
    messageCount['messageCount'] = document['messageCount']
    messageList.append(messageCount)
    level['level'] = document['level']
    messageList.append(level)
    UserId['UserId'] =document['UserId']
    messageList.append(UserId)
    follower['follower'] = document['follower']
    messageList.append(follower)
    summary['summary'] = document['summary']
    messageList.append(summary)
    user_work['user_work'] = document['user_work']
    messageList.append(user_work)
    following['following'] = document['following']
    messageList.append(following)
    user_name['user_name'] = document['user_name']
    messageList.append(user_name)
    #change the talkList
    for k in document['talkList']:
        tempList = messageList
        talkList['talkList'] = document['talkList'][k]
        messageLists.append(tempList)
    return messageLists


def txwbshow(num=10):
    client = pymongo.MongoClient("192.168.8.25", 27017)
    try:
        database = client["db_tx_wb_content"]
        table = database["t_weibo_content"]
        cursor = table.find().limit(num)
        messageLists = []
        for document in cursor:
            messageLists.append(catchdetail(document))
        return messageLists
    except Exception, e:
        print e
    finally:
        client.close()
        

if __name__ == '__main__':
    print txwbshow(num=10)