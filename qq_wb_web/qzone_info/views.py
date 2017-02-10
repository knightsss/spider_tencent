#coding=utf-8
from django.shortcuts import render,render_to_response

# Create your views here.
def qzone_info(request):

    render_to_response("qzone_info.html")

