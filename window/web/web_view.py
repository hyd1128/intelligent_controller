#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/5 17:51
# @Author : limber
# @desc :
import sys

from PyQt6.QtCore import QUrl, Qt, pyqtSlot
from PyQt6.QtGui import QShortcut, QKeySequence
from PyQt6.QtWebChannel import QWebChannel
from PyQt6.QtWebEngineCore import QWebEnginePage, QWebEngineSettings
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QApplication

from channel_handler.board_handler import BoardHandler
from channel_handler.login_handler import LoginHandler
from channel_handler.device_handler import DeviceHandler
from channel_handler.task_handler import TaskHandler
from channel_handler.tools_handler import ToolsHandler


class BrowserPage(QWidget):
    def __init__(self):
        super().__init__()
        self.web_view = QWebEngineView()
        self.channel = QWebChannel()
        # 实例化一个handler slot
        self.login_handler = LoginHandler()
        self.device_handler = DeviceHandler()
        self.board_handler = BoardHandler()
        self.task_handler = TaskHandler()
        self.tools_handler = ToolsHandler()


        self.dev_tools = QWebEngineView()
        self.dev_tools_page = QWebEnginePage()
        # 定义布局
        self.layout = QVBoxLayout()
        self.show_dev_page = False

        # 定义快捷键名称
        self.shortcut_f12 = None

        # 初始化界面
        self.init_ui()
        # 初始化web view
        self.init_web_view()
        # 绑定快捷键
        self.bind_short_cut()

    def init_ui(self):
        self.setLayout(self.layout)
        self.layout.addWidget(self.web_view)
        self.dev_tools.setPage(self.dev_tools_page)
        self.web_view.page().setDevToolsPage(self.dev_tools_page)
        self.layout.addWidget(self.dev_tools)
        self.dev_tools.hide()

    def init_web_view(self):
        # 这里添加所有的handler
        self.channel.registerObject("loginHandler", self.login_handler)
        self.channel.registerObject("deviceHandler", self.device_handler)
        self.channel.registerObject("boardHandler", self.board_handler)
        self.channel.registerObject("taskHandler", self.task_handler)
        self.channel.registerObject("toolsHandler", self.tools_handler)
        self.web_view.page().setWebChannel(self.channel)

        # 启用localstorage
        setting = self.web_view.page().settings()
        setting.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        self.web_view.load(QUrl("http://127.0.0.1:8000"))
        # self.web_view.load(QUrl("http://www.baidu.com"))

    def bind_short_cut(self):
        # 给界面绑定f12快捷键
        self.shortcut_f12 = QShortcut(QKeySequence(Qt.Key.Key_F12), self)
        # 绑定f12快捷键触发事件
        self.shortcut_f12.activated.connect(self.on_f12_pressed)

    @pyqtSlot()
    def on_f12_pressed(self):
        if self.show_dev_page:
            self.dev_tools.hide()
            self.show_dev_page = False
        else:
            self.dev_tools.show()
            self.show_dev_page = True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BrowserPage()
    window.show()
    sys.exit(app.exec())
