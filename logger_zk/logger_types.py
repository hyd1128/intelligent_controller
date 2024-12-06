#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/9/23 11:09
# @Author : limber
# @desc :
import logging
from logger_zk.logger_whole_situation import LoggerUtil

# 全局logger日志记录器
logger_main: logging.Logger = LoggerUtil().get_logger()
logger_watch: logging.Logger = LoggerUtil(log_file="./log/watch.log", logger_name="watch_thread").get_logger()
logger_run: logging.Logger = LoggerUtil(log_file="./log/run.log", logger_name="run_thread").get_logger()

