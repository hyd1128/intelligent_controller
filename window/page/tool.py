#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/11/1 13:43
# @Author : limber
# @desc :
from PyQt6 import QtWidgets
from PyQt6.QtGui import QTextCursor

from q_threads.del_app_thread import DeleteAppThread
from q_threads.update_app_thread import UpdateAppThread
from q_threads.download_app_thread import DownloadAppThread
from q_threads.authentication_app_thread import AuthenticationAppThread


class ToolPage:
    def __init__(self, parent):
        self.__parent = parent
        self.setup()

    def setup(self):
        # 加入父组件
        self.top_widget = QtWidgets.QWidget()
        self.__parent.widget.addWidget(self.top_widget)

        # 布局
        self.layout = QtWidgets.QVBoxLayout(self.top_widget)

        # 添加页面线程
        # 下载
        self.download_thread = DownloadAppThread()
        self.download_thread.signal.connect(self.show_log)
        # 删除
        self.del_thread = DeleteAppThread()
        self.del_thread.signal.connect(self.show_log)
        # 更新
        self.update_thread = UpdateAppThread()
        self.update_thread.signal.connect(self.show_log)
        # 鉴权
        self.authentication_thread = AuthenticationAppThread()
        self.authentication_thread.signal.connect(self.show_log)

        # 添加ui
        self.add_ui()

    # 添加操作
    def add_ui(self):
        self.widget = QtWidgets.QWidget(parent=self.top_widget)

        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.widget)

        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()

        self.widget_2 = QtWidgets.QWidget(parent=self.widget)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget_2)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.pushButton = QtWidgets.QPushButton(parent=self.widget_2)
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_5 = QtWidgets.QPushButton(parent=self.widget_2)
        self.horizontalLayout.addWidget(self.pushButton_5)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.pushButton.setText("下载app")
        self.pushButton_5.setText("停止")
        self.pushButton.clicked.connect(self.start_download_thread)
        self.pushButton_5.clicked.connect(self.stop_download_thread)


        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.widget_2)
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        self.pushButton_6 = QtWidgets.QPushButton(parent=self.widget_2)
        self.horizontalLayout_2.addWidget(self.pushButton_6)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.pushButton_2.setText("删除app")
        self.pushButton_6.setText("停止")
        self.pushButton_2.clicked.connect(self.start_del_thread)
        self.pushButton_6.clicked.connect(self.stop_del_thread)


        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.pushButton_3 = QtWidgets.QPushButton(parent=self.widget_2)
        self.horizontalLayout_3.addWidget(self.pushButton_3)
        self.pushButton_7 = QtWidgets.QPushButton(parent=self.widget_2)
        self.horizontalLayout_3.addWidget(self.pushButton_7)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.pushButton_3.setText("更新app")
        self.pushButton_7.setText("停止")
        self.pushButton_3.clicked.connect(self.start_update_thread)
        self.pushButton_7.clicked.connect(self.stop_update_thread)

        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.pushButton_4 = QtWidgets.QPushButton(parent=self.widget_2)
        self.horizontalLayout_6.addWidget(self.pushButton_4)
        self.pushButton_8 = QtWidgets.QPushButton(parent=self.widget_2)
        self.horizontalLayout_6.addWidget(self.pushButton_8)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.pushButton_4.setText("鉴权app")
        self.pushButton_8.setText("停止")
        self.pushButton_4.clicked.connect(self.start_authentication_thread)
        self.pushButton_8.clicked.connect(self.stop_authentication_thread)

        self.horizontalLayout_4.addWidget(self.widget_2)
        self.textBrowser = QtWidgets.QTextBrowser(parent=self.widget)
        self.horizontalLayout_4.addWidget(self.textBrowser)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_4)
        self.layout.addWidget(self.widget)

    # 开始删除app线程
    def start_del_thread(self):
        self.textBrowser.clear()
        if not self.del_thread.isRunning():
            if self.del_thread.flag == False:
                self.del_thread.flag = True
            self.del_thread.start()

    # 开启更新app线程
    def start_update_thread(self):
        self.textBrowser.clear()
        if not self.update_thread.isRunning():
            if self.update_thread.flag == False:
                self.update_thread.flag = True
            self.update_thread.start()

    # 开启下载app线程
    def start_download_thread(self):
        self.textBrowser.clear()
        if not self.download_thread.isRunning():
            if self.download_thread.flag == False:
                self.download_thread.flag = True
            self.download_thread.start()

    # 开启鉴权app线程
    def start_authentication_thread(self):
        self.textBrowser.clear()
        if not self.authentication_thread.isRunning():
            if self.authentication_thread.flag == False:
                self.authentication_thread.flag = True
            self.authentication_thread.start()

    # 停止删除app线程
    def stop_del_thread(self):
        if self.del_thread.flag:
            self.del_thread.flag = False

    # 停止更新app线程
    def stop_update_thread(self):
        if self.update_thread.flag:
            self.update_thread.flag = False

    # 停止下载app线程
    def stop_download_thread(self):
        if self.download_thread.flag:
            self.download_thread.flag = False

    # 停止鉴权app线程
    def stop_authentication_thread(self):
        if self.authentication_thread.flag:
            self.authentication_thread.flag = False

    # 将日志打印到程序框
    def show_log(self, msg):
        self.textBrowser.append(msg)
        self.textBrowser.moveCursor(QTextCursor.MoveOperation.End)







