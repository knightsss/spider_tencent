#coding=utf-8

from django.shortcuts import render,render_to_response

from qzone_friend.qzone_friend_thread import ThreadControl
from qzone_friend.models import Thread_qq_friend
from log.rtx import rtx,get_ip

# Create your views here.
def qzone_friend(request):
    #用于判断前端页面显示活跃状态
    friend_thread = True
    #获取本机IP
    IP = get_ip()
    thread_list = Thread_qq_friend.objects.filter(thread_ip=IP)
    for thread in thread_list:
        c  = ThreadControl()
        try:
            #查看是否处于活跃状态
            status = c.is_alive(thread.thread_name)
            if status:
                #设置状态为1
                thread.thread_status = 1
                thread.save()
            else:
                #设置状态为0
                thread.thread_status = 0
                thread.save()
        except:
            thread.thread_status = 0
            thread.save()
    return render_to_response("qzone_friend.html",{"thread_list":thread_list, "friend_thread":friend_thread})

def qzone_friend_all(request):
    #用于判断前端页面显示活跃状态
    all_friend_active = True
    thread_list = Thread_qq_friend.objects.all()
    return render_to_response("qzone_friend.html",{"thread_list":thread_list, "all_friend_active":all_friend_active})

def control_friend_thread(request):
    th_name = request.POST['id']
    control = request.POST['control']
    print "thread_name is ",th_name
    qzone_friend = True
    thread = Thread_qq_friend.objects.get(thread_name=th_name)
    if control == 'start':
        #状态信息
        rtx('ip','进程' + str(th_name) + '  开始采集关系链')
        # thread1_status = True
        c  = ThreadControl()
        # status = 1
        #出现错误，则线程不存在，因此启动线程
        try:
            status = c.is_alive(th_name)
            print "thread is alive? ",status
            if status:
                print "thread is alive,caonot start twice!"
            else:
                print "start ..........thread1"
                c.start(th_name,1)
        except:
            print "thread is not alive start!!!"
            c.start(th_name,1)
        thread.thread_status = 1
        thread.save()
    if control == 'stop':
        # thread1_status = False
        # status = 0
        rtx('ip','进程' + str(th_name) + '  采集关系链停止')
        c  = ThreadControl()
        try:
            c.stop(th_name)
            thread.thread_status = 0
            thread.save()
        except:
            print "not thread alive"

    IP = get_ip()
    thread_list = Thread_qq_friend.objects.filter(thread_ip=IP)
    return render_to_response('qzone_friend.html',{"thread_name":th_name, "control":control, "thread_list":thread_list,"qzone_friend":qzone_friend})