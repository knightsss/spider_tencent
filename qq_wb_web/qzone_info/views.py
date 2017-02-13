#coding=utf-8
from django.shortcuts import render,render_to_response
from log.rtx import get_ip,rtx
from qzone_info.models import ThreadQzoneInfo
from qzone_info.qq_info_thread import ThreadControl
# Create your views here.
def qzone_info(request):
    thread_status = False
    info_active = True
    IP = get_ip()
    thread_list = ThreadQzoneInfo.objects.filter(thread_ip=IP)
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
    return render_to_response('qzone_info.html',{"info_active":info_active , "thread_list":thread_list})
    # render_to_response("qzone_info.html")

def qzone_info_all(request):
    thread_list = ThreadQzoneInfo.objects.all()
    all_info_active = True
    return render_to_response('qzone_info.html',{"all_info_active":all_info_active, "thread_list":thread_list})


def control_qzone_info_thread(request):
    th_name = request.POST['id']
    control = request.POST['control']
    print "thread_name is ",th_name
    #显示活跃状态
    info_active = True
    thread = ThreadQzoneInfo.objects.get(thread_name=th_name)
    if control == 'start':
        rtx('ip','进程' + str(th_name) + '  开始采集标签信息')
        #状态信息
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
        rtx('ip','进程' + str(th_name) + '  采集标签信息即将停止')
        c  = ThreadControl()
        try:
            c.stop(th_name)
            thread.thread_status = 0
            thread.save()
        except:
            print "not thread alive"

    IP = get_ip()
    thread_list = ThreadQzoneInfo.objects.filter(thread_ip=IP)
    return render_to_response('qzone_info.html',{"thread_name":th_name, "control":control, "thread_list":thread_list,"info_active":info_active})
