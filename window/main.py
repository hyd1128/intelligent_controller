import os.path
import sys
from typing import Any

from PyQt6 import QtWidgets
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow
from window.navbar.main import Navbar
from window.page.main import Page
from watch import New, Offline
from window.dialog.new_device import NewDeviceDialog
from window.dialog.offline_device import OfflineDeviceDialog
from run.run_sync import Run
from util.utils import queue_store_device_detail_config
from window.web.web_view import BrowserPage
from client_controller.main_controller import MainController
from util.info_util import get_node_info, edit_node_info
from util.identify_util import generate_unique_node_token


class Main(QMainWindow):

    def __init__(self):
        super().__init__()
        # 定义容器
        self.widget = None
        # 定义布局
        self.layout = None
        # 定义线程
        self.watch_new = None
        self.watch_offline = None
        self.run_task = None
        self.main_controller = None
        # 定义组件
        self.browser = None
        self.setup()

    def setup(self):
        # 初始化窗口
        self.resize(1200, 600)
        self.setWindowTitle("智控管家")
        self.setWindowIcon(QIcon("app/icon/quanqiu.png"))

        # 判断该节点是否具有唯一标识 如果没有 则生成并添加
        # node_info_path = os.path.join(sys.path[1] + "/node_info/info.json")
        node_info_path = "./node_info/info.json"
        node_info = get_node_info(node_info_path)
        if not node_info["node_id"]:
            node_info["node_id"] = generate_unique_node_token()
            edit_node_info(node_info_path, node_info)

        # 容器
        self.widget = QtWidgets.QWidget(parent=self)
        self.setCentralWidget(self.widget)

        # 容器布局
        self.layout = QtWidgets.QHBoxLayout(self.widget)
        self.layout.setContentsMargins(0, 0, 0, 10)
        self.layout.setSpacing(0)

        # 初始化全局队列
        queue_store_device_detail_config()

        # # 引入子组件
        # self.navbar()
        # self.pages()
        self.browser = BrowserPage()
        self.layout.addWidget(self.browser)

        # 监听新设备
        self.watch_new = New()
        self.watch_new.signal.connect(self.dialog_new_device)
        self.watch_new.start()

        # 监听掉线设备
        self.watch_offline = Offline()
        self.watch_offline.signal.connect(self.dialog_offline_device)
        self.watch_offline.start()

        # 执行任务
        self.run_task = Run()
        self.run_task.start()

        # 启动定时上传任务
        self.main_controller = MainController()
        self.main_controller.start()

    def closeEvent(self, event):
        self.watch_new.stop()
        self.watch_offline.stop()
        self.run_task.stop()
        self.main_controller.stop()

        # node_info_path = os.path.join(sys.path[1] + "/node_info/info.json")
        # current_user_detail_path = os.path.join(sys.path[1] + "/node_info/current_user_detail.json")
        node_info_path = "./node_info/info.json"
        current_user_detail_path = "./node_info/current_user_detail.json"
        node_info = get_node_info(node_info_path)
        node_info["normal_account"] = ""
        node_info["password"] = ""
        node_info["top_account"] = ""
        edit_node_info(node_info_path, node_info)
        current_user_detail = {}
        edit_node_info(current_user_detail_path, current_user_detail)
        event.accept()

    def change_page(self, index):
        """切换页面"""

        self.page.change_page(index)

    def navbar(self):
        """菜单栏"""

        Navbar(self)

    def pages(self):
        """页面"""

        self.page = Page(self)

    def dialog_new_device(self, msg):
        """新设备弹窗"""

        # NewDeviceDialog(msg, self).exec()
        # msg是新设备详细信息
        NewDeviceDialog(msg, self).add()

    def set_device_page_data(self):
        """刷新设备列表"""

        self.page.set_device_page_data()

    def dialog_offline_device(self, msg):
        """掉线设备弹窗"""

        # 更新设备列表
        self.page.set_device_page_data()

        # 更新，设备掉线不弹框
        #
        # 如果设备离线，则弹框
        # if msg["online"] == "offline":
        #     OfflineDeviceDialog(msg).exec()
