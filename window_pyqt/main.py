# coding:utf-8
import sys
from PyQt6.QtCore import Qt, QRect, QUrl
from PyQt6.QtGui import QIcon, QPainter, QImage, QBrush, QColor, QFont, QDesktopServices
from PyQt6.QtWidgets import QApplication, QFrame, QStackedWidget, QHBoxLayout, QLabel

from qfluentwidgets import (NavigationInterface, NavigationItemPosition, NavigationWidget, MessageBox,
                            isDarkTheme, setTheme, Theme, qrouter)
from qfluentwidgets import FluentIcon as FIF
from qframelesswindow import FramelessWindow, TitleBar

from qt_threads.new_device_monitor import NewDeviceMonitor
from qt_threads.offline_device_monitor import OfflineDeviceMonitor
from qt_threads.run_advertising_thread import RunAdvertisingThread
from util.queue_util import DeviceQueueUtil
from window_pyqt.component.avator_widget import AvatarWidget
from window_pyqt.component.custom_title_bar_widget import CustomTitleBar
from window_pyqt.component.general_widget import Widget
from window_pyqt.component.message_widget import MessageWidget
from window_pyqt.view.advertising_task_record_table_view import AdvertisingTaskRecordTableView
from window_pyqt.view.advertising_task_table_view import AdvertisingTaskTableView
from window_pyqt.view.app_table_view import AppTableView
from window_pyqt.view.app_task_record_table_view import AppTaskRecordTableView
from window_pyqt.view.app_task_table_view import AppTaskTableView
from window_pyqt.view.device_table_view import DeviceTableView
from window_pyqt.view.home_view import HomeView
from window_pyqt.view.script_table_view import ScriptTableView
from util import config_util


class Window(FramelessWindow):

    def __init__(self):
        super().__init__()
        self.setTitleBar(CustomTitleBar(self))

        # use dark theme mode
        # setTheme(Theme.DARK)

        self.hBoxLayout = QHBoxLayout(self)
        self.navigationInterface = NavigationInterface(
            self, showMenuButton=True, showReturnButton=False)
        self.stackWidget = QStackedWidget(self)

        # create sub interface
        # self.searchInterface = Widget('Search Interface', self)
        self.homeView = HomeView('Home View', self)
        self.deviceView = DeviceTableView('Device Table View', self)
        self.appView = AppTableView('App Table View', self)
        self.appTaskView = AppTaskTableView('App Task Table View', self)
        self.appTaskRecordView = AppTaskRecordTableView('App Task Record Table View', self)
        self.advertisingTaskView = AdvertisingTaskTableView('Advertising Task Table View', self)
        self.advertisingTaskRecordView = AdvertisingTaskRecordTableView('Advertising Task Record Table View', self)
        self.scriptView = ScriptTableView('Script TableView', self)

        """
        槽函数关联信号
        """
        self.homeView.run_advertising_switch_signal.connect(self.run_advertising_signal)


        """
        这里添加各类线程和初始化
        界面以外的东西这里启动
        """
        ##################################
        # 初始化全局队列
        DeviceQueueUtil.initialize_device_queue()
        # 监听新设备
        self.watch_new = NewDeviceMonitor()
        self.watch_new.new_device_signal.connect(self.new_device_signal)
        self.watch_new.start()

        # 监听掉线设备
        self.watch_offline = OfflineDeviceMonitor()
        self.watch_offline.device_online_signal.connect(self.device_online_signal)
        self.watch_offline.device_offline_signal.connect(self.device_offline_signal)
        self.watch_offline.start()

        # 执行任务
        self.run_task = RunAdvertisingThread()
        self.run_task.start()

        ##################################

        # initialize layout
        self.initLayout()

        # add items to navigation interface
        self.initNavigation()

        self.initWindow()

    def initLayout(self):
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        # 添加左侧导航栏
        self.hBoxLayout.addWidget(self.navigationInterface)
        # 添加一个控件
        self.hBoxLayout.addWidget(self.stackWidget)
        self.hBoxLayout.setStretchFactor(self.stackWidget, 1)

        # 将导航栏放到最前面
        self.titleBar.raise_()
        self.navigationInterface.displayModeChanged.connect(self.titleBar.raise_)

    def initNavigation(self):
        # enable acrylic effect
        # self.navigationInterface.setAcrylicEnabled(True)
        self.addSubInterface(self.homeView, FIF.HOME, "主界面")
        self.addSubInterface(self.deviceView, FIF.PHONE, '设备列表')
        self.addSubInterface(self.appView, FIF.APPLICATION, '应用列表')
        self.addSubInterface(self.appTaskView, FIF.RINGER, '应用任务列表')
        self.addSubInterface(self.appTaskRecordView, FIF.COMPLETED, '应用任务列表记录')
        self.addSubInterface(self.advertisingTaskView, FIF.RINGER, '广告任务列表')
        self.addSubInterface(self.advertisingTaskRecordView, FIF.COMPLETED, '广告任务记录列表')
        self.addSubInterface(self.scriptView, FIF.FOLDER, '脚本列表')
        # for i in range(1, 21):
        #     self.navigationInterface.addItem(
        #         f'folder{i}',
        #         FIF.FOLDER,
        #         f'Folder {i}',
        #         lambda: print('Folder clicked'),
        #         position=NavigationItemPosition.SCROLL
        #     )

        # add custom widget to bottom
        # self.navigationInterface.addWidget(
        #     routeKey='avatar',
        #     widget=AvatarWidget(),
        #     onClick=self.showMessageBox,
        #     position=NavigationItemPosition.BOTTOM
        # )

        # self.addSubInterface(self.settingInterface, FIF.SETTING, 'Settings', NavigationItemPosition.BOTTOM)

        # !IMPORTANT: don't forget to set the default route key
        qrouter.setDefaultRouteKey(self.stackWidget, self.homeView.objectName())

        # set the maximum width
        # self.navigationInterface.setExpandWidth(300)

        self.stackWidget.currentChanged.connect(self.onCurrentInterfaceChanged)
        self.stackWidget.setCurrentIndex(0)

    def initWindow(self):
        self.resize(900, 700)
        self.setWindowIcon(QIcon('resources/resource/logo.png'))
        # self.setWindowTitle('PyQt-Fluent-Widgets')
        self.setWindowTitle('智控管家app')
        self.titleBar.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

        self.setQss()

    def addSubInterface(self, interface, icon, text: str, position=NavigationItemPosition.TOP):
        """ add sub interface """
        self.stackWidget.addWidget(interface)
        self.navigationInterface.addItem(
            routeKey=interface.objectName(),
            icon=icon,
            text=text,
            onClick=lambda: self.switchTo(interface),
            position=position,
            tooltip=text
        )

    def setQss(self):
        color = 'dark' if isDarkTheme() else 'light'
        with open(f'resources/resource/{color}/demo.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def switchTo(self, widget):
        self.stackWidget.setCurrentWidget(widget)

    def onCurrentInterfaceChanged(self, index):
        widget = self.stackWidget.widget(index)
        if widget.objectName() != 'Home-View':
            # print(widget.objectName())
            widget.update_page()
        else:
            # print(widget.objectName())
            pass
        self.navigationInterface.setCurrentItem(widget.objectName())
        qrouter.push(self.stackWidget, widget.objectName())

    def showMessageBox(self):
        w = MessageBox(
            '支持作者🥰',
            '个人开发不易，如果这个项目帮助到了您，可以考虑请作者喝一瓶快乐水🥤。您的支持就是作者开发和维护项目的动力🚀',
            self
        )
        w.yesButton.setText('来啦老弟')
        w.cancelButton.setText('下次一定')

        if w.exec():
            QDesktopServices.openUrl(QUrl("https://afdian.net/a/zhiyiYo"))

    def resizeEvent(self, e):
        self.titleBar.move(46, 0)
        self.titleBar.resize(self.width() - 46, self.titleBar.height())

    def new_device_signal(self, device_):
        self.deviceView.update_page()
        MessageWidget.info_message(self, f"发现新设备, 设备名称为 {device_.device_id}")

    def device_online_signal(self, device_):
        self.deviceView.update_page()
        MessageWidget.info_message(self, f"设备 {device_.device_id}已连接")

    def device_offline_signal(self, device_):
        self.deviceView.update_page()
        MessageWidget.info_message(self, f"设备 {device_.device_id}已掉线")

    def run_advertising_signal(self, is_open):
        if is_open:
            print("####启动广告任务...####")
            config_util.SWITCH = True
        else:
            print("####关闭广告任务...####")
            config_util.SWITCH = False

    def closeEvent(self, event):
        self.watch_new.stop()
        self.watch_offline.stop()
        self.run_task.stop()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec()
