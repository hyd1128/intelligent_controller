from PyQt6 import QtWidgets
import global_var
from logger_zk.logger_types import logger_main


class Navbar:
    def __init__(self, parent):
        self.__parent = parent
        self.setup()

    def setup(self):
        # 创建一个容器控件并设置父容器
        self.widget = QtWidgets.QFrame(parent=self.__parent.widget)
        self.__parent.layout.addWidget(self.widget)
        # 样式
        self.widget.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.widget.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.widget.setLineWidth(0)

        # 尺寸策略
        size_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
        size_policy.setHorizontalStretch(1)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(size_policy)

        # 垂直布局
        self.layout = QtWidgets.QVBoxLayout(self.widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(10)

        # 引入子控件
        self.device_btn()
        self.app_btn()
        self.script_btn()
        self.task_btn()
        self.task_device_btn()
        self.tool_btn()
        self.spacer()
        self.task_running_btn()

    def device_btn(self):
        """设备列表按钮控件"""

        # 创建一个按钮控件并设置父控件
        btn = QtWidgets.QPushButton(parent=self.widget)
        self.layout.addWidget(btn)
        # 设置文本
        btn.setText("设备列表")
        # 点击事件
        btn.clicked.connect(lambda: self.__parent.change_page(0))

    def app_btn(self):
        """应用列表按钮控件"""

        btn = QtWidgets.QPushButton(parent=self.widget)
        self.layout.addWidget(btn)
        btn.setText("应用列表")
        btn.clicked.connect(lambda: self.__parent.change_page(1))

    def script_btn(self):
        """脚本列表按钮控件"""

        btn = QtWidgets.QPushButton(parent=self.widget)
        self.layout.addWidget(btn)
        btn.setText("脚本列表")
        btn.clicked.connect(lambda: self.__parent.change_page(2))

    def task_btn(self):
        """任务列表按钮控件"""

        btn = QtWidgets.QPushButton(parent=self.widget)
        self.layout.addWidget(btn)
        btn.setText("任务列表")
        btn.clicked.connect(lambda: self.__parent.change_page(3))

    def task_device_btn(self):
        """任务列表按钮控件"""

        btn = QtWidgets.QPushButton(parent=self.widget)
        self.layout.addWidget(btn)
        btn.setText("运行记录")
        btn.clicked.connect(lambda: self.__parent.change_page(4))

    def task_running_btn(self):
        """运行群控按钮控件"""

        self.btn_isrunning = QtWidgets.QPushButton(parent=self.widget)
        self.layout.addWidget(self.btn_isrunning)
        btn_text = "运行任务" if not global_var.is_running else "停止任务"
        self.btn_isrunning.setText(btn_text)
        self.btn_isrunning.clicked.connect(self.is_running_task)

    def spacer(self):
        """垂直弹簧控件"""

        spacer = QtWidgets.QSpacerItem(
            20, 40,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
        self.layout.addItem(spacer)

    def is_running_task(self):
        global_var.is_running = not global_var.is_running
        logger_main.info(f"*开关状态*===> {global_var.is_running}")
        if self.btn_isrunning.text() == "运行任务":
            self.btn_isrunning.setText("停止任务")
        else:
            self.btn_isrunning.setText("运行任务")

    # todo: 添加一个下载，更新，删除，权限管理app的页面
    def tool_btn(self):
        """app管理界面"""

        btn = QtWidgets.QPushButton(parent=self.widget)
        self.layout.addWidget(btn)
        btn.setText("工具管理界面")
        btn.clicked.connect(lambda: self.__parent.change_page(5))

