from django.shortcuts import render

# Create your views here.
import logging
import logging.config
import os

def log_setting_base(file_name):
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

def log_setting(file_name):
    logger_name = file_name[0:-4]
    print logger_name
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    # create file handler
    file_abspath = os.getcwd() + "\\log\\"
    log_path = file_abspath + file_name
    fh = logging.FileHandler(log_path)
    fh.setLevel(logging.INFO)

    # create formatter
    fmt = "%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s"
    datefmt = "%a %d %b %Y %H:%M:%S"
    formatter = logging.Formatter(fmt, datefmt)

    # add handler and formatter to logger
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger

