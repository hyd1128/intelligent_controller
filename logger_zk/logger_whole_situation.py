#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/9/23 9:31
# @Author : limber
# @desc :
import logging
from logging.handlers import RotatingFileHandler


class LoggerUtil:
    def __init__(self, log_file='./log/main.log', max_bytes=1024 * 1024, backup_count=10, logger_name="main"):
        # 创建一个日志记录器
        self.logger = logging.getLogger(logger_name)
        # 设置日志记录级别
        self.logger.setLevel(logging.DEBUG)

        # 禁用日志传播
        self.logger.propagate = False

        # 检查是否已有处理器，避免重复添加
        if not self.logger.hasHandlers():
            # 检查并移除已有处理器
            if self.logger.hasHandlers():
                for handler in self.logger.handlers[:]:  # 遍历并复制列表，避免修改时出错
                    self.logger.removeHandler(handler)
                    handler.close()  # 关闭处理器以释放资源

        # 设置日志格式，时间显示到秒
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # 创建控制台处理器，输出到标准输出
        console_handler = logging.StreamHandler()
        # 控制台输出级别
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        # 设置格式器
        self.logger.addHandler(console_handler)

        # 创建文件处理器，输出到文件，支持日志轮转
        file_handler = RotatingFileHandler(
            log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8", mode="w"
        )
        # 文件输出级别
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        # 设置格式器
        self.logger.addHandler(file_handler)

    def get_logger(self):
        return self.logger






