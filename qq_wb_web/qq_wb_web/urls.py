from django.conf.urls import patterns, include, url

from django.contrib import admin
from qq_wb_msg.views import index,control_thread, stop_thread, test_model
from wb_get_wid.views import auditor,control_auditor
from qq_wb_msg.views import thread_msg_all
from wb_get_wid.views import thread_auditor_all

import settings
from main.views import main
from qzone_friend.views import qzone_friend,qzone_friend_all,control_friend_thread
from qzone_info.views import qzone_info,qzone_info_all,control_qzone_info_thread

from show_message.views import show_tencent_wb_msg,show_qzone_info,show_tencent_wb_content,show_qzone_content,show_sina_info

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'qq_wb_web.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),
    url(r'^index/',index),
    url(r'^control_thread/$',control_thread),
    url(r'^test_model/$',test_model),

    url(r'^auditor/$',auditor),
    url(r'^control_auditor_thread/$',control_auditor),
    url(r'^thread_msg_all/$',thread_msg_all),
    url(r'^thread_auditor_all/$',thread_auditor_all),

    url(r'^main/$',main),

    url(r'^qzone_friend/$',qzone_friend),
    url(r'^qzone_friend_all/$',qzone_friend_all),
    url(r'^control_friend_thread/$',control_friend_thread),


    url(r'^qzone_info/$',qzone_info),
    url(r'^qzone_info_all/$',qzone_info_all),
    url(r'^control_qzone_info_thread/$',control_qzone_info_thread),


    # url(r'^show_message',show_message),

    url(r'^show_message/tencent_wb_msg/$',show_tencent_wb_msg),
    url(r'^show_message/qzone_info/$',show_qzone_info),
    url(r'^show_message/tencent_wb_content/$',show_tencent_wb_content),
    url(r'^show_message/qzone_content/$',show_qzone_content),
    url(r'^show_message/sina_info/$',show_sina_info),



    # url(r'^stop_thread/$',control_thread),
    # url(r'^delete_url/$', delete_url),
    url( r'^static/(?P<path>.*)$', 'django.views.static.serve',{ 'document_root': settings.STATIC_URL }),
)
