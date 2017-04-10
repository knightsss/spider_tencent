#coding=utf-8
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render_to_response
# Create your models here.
from pymongo import MongoClient
from db.db_mongodb import connect_mongodb_8_25,connect_mongodb_15_111

import sys
import json
print sys.getdefaultencoding()
import copy


def get_message(mongodb_client,db_name,tab_name,count):
    db = mongodb_client[db_name]
    t_name = db[tab_name]
    message_list = t_name.find().limit(count)
    return message_list

#腾讯微博信息展示
def show_tencent_wb_msg(request):

    # c = MongoClient()
    try:
        count = int(request.GET["count"])
    except:
        count = 100

    # mongodb_client = MongoClient('192.168.15.111',27017)

    mongodb_client = connect_mongodb_15_111()
    db_name = "db_tx_wb_msg"
    tab_name = "t_tencent_wb_msg3"

    #获取所有信息
    tencent_wb_msgs = get_message(mongodb_client,db_name,tab_name,count)
    tencent_wb_msg_list = []

    flag_str = "分享标签"
    count = 0
    for msg in tencent_wb_msgs:
        if msg["info"] != None:
            if flag_str in msg['info'].encode('utf-8'):
                # tencent_wb_msg_list.append(msg['info'].encode('utf-8'))
                tencent_wb_msg_list.append(msg)
                count = count + 1
    mongodb_client.close()
    print count
    print type(tencent_wb_msg_list)
    return render_to_response("show_message.html",{"tencent_wb_msg_list":tencent_wb_msg_list, "tencent_wb_msg_flag":True})

#QQ空间信息展示
def show_qzone_info(request):
    try:
        count = int(request.GET["count"])
    except:
        count = 30

    #定义连接、数据库名、表名
    mongodb_client = connect_mongodb_15_111()
    db_name = "db_tx_qzone_info"
    tab_name = "t_tencent_qzone_info"

    #获取所有信息
    tencent_qzone_infos = get_message(mongodb_client,db_name,tab_name,count)
    tencent_qzone_infos_list = []
    # print t_tencent_qzone_infos.find_one()
    for info in tencent_qzone_infos:
        info_dict = {}
        count = 0
        infos = ''
        for msg in info["info"]:
            if count > 0:
                infos = infos + msg
            count = count + 1
        name = info["info"][0]
        info_dict["info"] = infos

        info_dict["qq"] = info["qq"]
        info_dict["name"] = name
        info_dict["age"] = info["info"][5]
        info_dict["birthday"] = info["info"][6]
        info_dict["live_address"] = info["info"][8]
        info_dict["marriage"] = info["info"][9]
        info_dict["hometown_address"] = info["info"][11]
        if len(info["info"][13].encode('utf-8')) > 50:
            info_dict["company"] = "未正确填写"
        else:
            info_dict["company"] = info["info"][13]
        info_dict["career"] = info["info"][12]
        tencent_qzone_infos_list.append(info_dict)
    mongodb_client.close()
    return render_to_response("show_message.html",{"tencent_qzone_infos_list":tencent_qzone_infos_list, "tencent_qzone_info_flag":True})



def catchdetail(tencent_qzone_contents):
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

    messageLists = []
    for document in tencent_qzone_contents:
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
                if type(cont) is list:
                    tempDict[key] = json.dumps(cont,ensure_ascii=False,indent=2)
                else:
                    tempDict[key] = cont
            messageLists.append(tempDict.copy())

    return messageLists

def show_tencent_wb_content(request):
    try:
        count = int(request.GET["count"])
    except:
        count = 10
    mongodb_client = connect_mongodb_8_25()
    db_name = "db_tx_wb_content"
    tab_name = "t_weibo_content"
    tencent_qzone_contents = get_message(mongodb_client,db_name,tab_name,count)

    #获取所有发表内容
    messageLists = catchdetail(tencent_qzone_contents)
    tencent_wb_content_list = messageLists
    mongodb_client.close()
    return render_to_response("show_message.html",{"tencent_wb_content_list":tencent_wb_content_list, "tencent_wb_content_flag":True})


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
                # tempDict[key_c] = val_c
                tempDict[key_c] = json.dumps(val_c,ensure_ascii=False,indent=2)
            tempList.append(copy.deepcopy(tempDict))
    return tempList

#QQ空间说说
def show_qzone_content(request):
    tencent_qzone_content_list = []
    try:
        count = int(request.GET["count"])
    except:
        count = 10
    mongodb_client = connect_mongodb_8_25()
    db_name = "db_shuoshuo_content"
    tab_name = "t_shuoshuo_content"
    tencent_qzone_contents = get_message(mongodb_client,db_name,tab_name,count)
    tencent_qzone_content_list = getshuoshuoDetail(tencent_qzone_contents)

    return render_to_response("show_message.html",{"tencent_qzone_content_list":tencent_qzone_content_list, "tencent_qzone_content_flag":True})


def getsinawbDetail(cursor):
    messageLists = []
    for document in cursor:
        for key,value in document.items():
            if key == "_id":
                document["id"] = value
            # print type(value),value
            if type(value) is list:
                # print "list"
                value1 = json.dumps(value,ensure_ascii=False,indent=2)
                document[key] = value1
            else:
                pass

        messageLists.append(document.copy())
    return messageLists

#新浪微博
def show_sina_info(request):
    tencent_qzone_content_list = []
    try:
        count = int(request.GET["count"])
    except:
        count = 20
    mongodb_client = connect_mongodb_8_25()
    db_name = "db_sina_wb"
    tab_name = "t_youxi_labels"
    sina_wb_infos = get_message(mongodb_client,db_name,tab_name,count)
    sina_wb_infos_list = getsinawbDetail(sina_wb_infos)

    return render_to_response("show_message.html",{"sina_wb_infos_list":sina_wb_infos_list, "sina_wb_info_flag":True})


