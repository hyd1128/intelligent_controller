from datetime import datetime
from PyQt6 import QtWidgets
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow

from database_service.service.advertising_task_service import AdvertisingTaskService
from database_service.service.device_service import DeviceService
from util.config_util import RESOURCES, NODE_DATA
from util.http_util import HttpUtils
from util.path_util import PathUtil
from util.queue_util import DeviceQueueUtil
from window_webview.web.web_view import BrowserPage
from client_controller.main_controller import MainController
from util.file_util import FileUtil
from util.identify_util import generate_unique_node_token
from qt_threads.new_device_monitor import NewDeviceMonitor
from qt_threads.offline_device_monitor import OfflineDeviceMonitor
from qt_threads.run_advertising_thread import RunAdvertisingThread


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
        self.setWindowIcon(QIcon(f"{RESOURCES}/icon/quanqiu.png"))

        # 判断该节点是否具有唯一标识 如何是初始打开该软件 则生成唯一ID
        root_path = PathUtil.get_current_file_absolute_path(__file__).parent.parent
        node_info_path = root_path.joinpath(NODE_DATA)
        node_info = FileUtil.read_file_content(node_info_path)
        if not node_info["node_id"]:
            node_info["node_id"] = generate_unique_node_token()
            FileUtil.write_file_content(node_info_path, node_info)

        # 容器
        self.widget = QtWidgets.QWidget(parent=self)
        self.setCentralWidget(self.widget)

        # 容器布局
        self.layout = QtWidgets.QHBoxLayout(self.widget)
        self.layout.setContentsMargins(0, 0, 0, 10)
        self.layout.setSpacing(0)

        # 初始化全局队列
        DeviceQueueUtil.initialize_device_queue()

        # 引入子组件
        self.browser = BrowserPage()
        self.layout.addWidget(self.browser)

        # 监听新设备
        self.watch_new = NewDeviceMonitor()
        self.watch_new.start()

        # 监听掉线设备
        self.watch_offline = OfflineDeviceMonitor()
        self.watch_offline.start()

        # 执行任务
        self.run_task = RunAdvertisingThread()
        self.run_task.start()

        # 启动定时上传任务
        self.main_controller = MainController()
        self.main_controller.start()

    def closeEvent(self, event):
        self.watch_new.stop()
        self.watch_offline.stop()
        self.run_task.stop()
        self.main_controller.stop()

        root_path = PathUtil.get_current_file_absolute_path(__file__).parent.parent
        node_info_path = root_path.joinpath("NODE_DATA")
        current_user_detail_path = root_path.joinpath("CURRENT_USER_DETAIL")
        node_info = FileUtil.read_file_content(node_info_path)
        update_node_info = {
            "normal_account": "",
            "password": "",
            "top_account": ""
        }

        # 关闭窗口后更新节点状态
        # 定时更新节点信息
        suitable_devices = DeviceService.select_by_online_state(online_state=1)
        latest_tasks = AdvertisingTaskService.select_all()
        is_update_latest = 0
        latest_task = ""
        if latest_tasks:
            latest_task = latest_tasks[-1]
            latest_task_release_date = datetime.strptime(latest_task.task_release_date, "%Y-%m-%d").date()
            today_ = datetime.now().date()
            is_update_latest = 1 if today_ == latest_task_release_date else 0
        online_device = len(suitable_devices)

        # 当前节点信息
        node_data = {
            "uuid": node_info["node_id"],  # 节点ID
            "node_version": node_info["node_version"],  # 节点版本
            "normal_accounts": node_info["normal_account"],  # 当前登录节点的普通账号
            "top_accounts": node_info["top_account"],  # 普通账号所属的顶级账号
            "online_device": str(online_device),  # 在线设备数
            "status": 0,  # 1:节点在线  0:节点离线
            "task_version": latest_task.task_release_date if latest_task else "",  # 当前执行的任务版本
            "update_task": is_update_latest  # 1: 已更新最新任务 0: 未更新最新任务
        }

        UPDATE_NODE_URI = "/api/v1/root_accounts/device/node"
        HttpUtils.post(UPDATE_NODE_URI, json_data=node_data)

        # 关闭窗口后置空登录用户
        node_info = {**node_info, **update_node_info}
        FileUtil.write_file_content(node_info_path, node_info)

        # 关闭窗口给后置空当前登录用户
        current_user_detail = {}
        FileUtil.write_file_content(current_user_detail_path, current_user_detail)
        event.accept()
