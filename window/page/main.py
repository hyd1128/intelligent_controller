from PyQt6 import QtWidgets
from window.page.device import DevicePage
from window.page.app import AppPage
from window.page.script import ScriptPage
from window.page.task import TaskPage
from window.page.task_device import TaskDevicePage
from window.page.tool import ToolPage


class Page:
    def __init__(self, parent):
        self.__parent = parent
        self.setup()

    def setup(self):
        # 加入父容器
        main_widget = QtWidgets.QFrame(parent=self.__parent.widget)
        self.__parent.layout.addWidget(main_widget)

        # 样式
        main_widget.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        main_widget.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        main_widget.setLineWidth(0)

        # 尺寸策略
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred,
                                            QtWidgets.QSizePolicy.Policy.Expanding)
        size_policy.setHorizontalStretch(5)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(main_widget.sizePolicy().hasHeightForWidth())
        main_widget.setSizePolicy(size_policy)

        # 布局
        main_layout = QtWidgets.QGridLayout(main_widget)
        main_layout.setContentsMargins(10, 0, 0, 0)
        main_layout.setSpacing(0)

        # 控件容器
        self.widget = QtWidgets.QStackedWidget(parent=main_widget)
        self.widget.setLineWidth(0)
        main_layout.addWidget(self.widget)

        # 引入子控件
        self.device()
        self.app()
        self.script()
        self.task()
        self.task_device()
        self.tool()

        # 设置默认显示页面
        self.widget.setCurrentIndex(0)

    def change_page(self, index):
        self.widget.setCurrentIndex(index)
        if index == 0:
            self.set_device_page_data()
        if index == 1:
            self.app_page.set_table_data()
        if index == 2:
            self.script_page.set_table_data()
        if index == 3:
            self.task_page.set_table_data()
        if index == 4:
            self.task_device_page.set_table_data()
        # if index == 5:
        #     self.tool_page

    def tool(self):
        self.tool_page = ToolPage(self)

    def device(self):
        self.device_page = DevicePage(self)

    def set_device_page_data(self):
        self.device_page.set_table_data()

    def app(self):
        self.app_page = AppPage(self)

    def script(self):
        self.script_page = ScriptPage(self)

    def task(self):
        self.task_page = TaskPage(self)

    def task_device(self):
        self.task_device_page = TaskDevicePage(self)
