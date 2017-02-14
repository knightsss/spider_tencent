from django.shortcuts import render

# Create your views here.
import logging
import logging.config
import os



def log_setting(file_name):
    ##############linux
    file_abspath = os.getcwd() + "/log/"
    ##############windows
    # file_abspath = os.getcwd() + "\\log\\"
    # print "file_abspath",file_abspath
    logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename= file_abspath + file_name,
                    filemode='a')

    return logging

