from PyQt6 import QtWidgets, QtCore
from store_service.service.service_device import DeviceService


class DevicePage:
    online = "all"  # 状态筛选
    task = "all"  # 是否有任务筛选

    def __init__(self, parent):
        self.__parent = parent
        self.page_number = 0
        self.items_ = 15

        self.setup()

    def setup(self):

        # 加入父组件
        self.widget = QtWidgets.QWidget()
        self.__parent.widget.addWidget(self.widget)

        # 布局
        self.layout = QtWidgets.QVBoxLayout(self.widget)

        # 引入子组件
        self.search_status()
        self.search_task()
        self.table_widget()

        # 初始化数据
        self.set_table_data()

        # 引入切换页面的组件
        self.page_widget()

    def search_status(self):
        """状态查询"""

        # 布局
        layout = QtWidgets.QHBoxLayout()
        layout.setSpacing(10)
        # 加入父布局
        self.layout.addLayout(layout)
        # 描述
        label = QtWidgets.QLabel(parent=self.widget)
        label.setText("在线状态")
        layout.addWidget(label)
        # 所有
        all_radio = QtWidgets.QRadioButton(parent=self.widget)
        all_radio.setText("全部")
        layout.addWidget(all_radio)
        # 默认选中
        all_radio.setChecked(True)
        all_radio.toggled.connect(lambda: self.do_search_online("all"))

        # 在线
        online_radio = QtWidgets.QRadioButton(parent=self.widget)
        online_radio.setText("在线")
        layout.addWidget(online_radio)
        online_radio.toggled.connect(lambda: self.do_search_online("online"))

        # 离线
        offline_radio = QtWidgets.QRadioButton(parent=self.widget)
        offline_radio.setText("离线")
        layout.addWidget(offline_radio)
        offline_radio.toggled.connect(lambda: self.do_search_online("offline"))

        # 分组
        radio_group = QtWidgets.QButtonGroup(self.widget)
        radio_group.setExclusive(True)
        radio_group.addButton(all_radio)
        radio_group.addButton(online_radio)
        radio_group.addButton(offline_radio)

        # 弹簧
        spacer = QtWidgets.QSpacerItem(40, 20,
                                       QtWidgets.QSizePolicy.Policy.Expanding,
                                       QtWidgets.QSizePolicy.Policy.Minimum
                                       )
        layout.addItem(spacer)

    def do_search_online(self, online):
        self.online = online
        self.set_table_data()

    # 任务查询
    def search_task(self):
        # 布局
        layout = QtWidgets.QHBoxLayout()
        layout.setSpacing(10)
        # 加入父布局
        self.layout.addLayout(layout)
        # 描述
        label = QtWidgets.QLabel(parent=self.widget)
        label.setText("任务状态")
        layout.addWidget(label)
        # 所有
        all_radio = QtWidgets.QRadioButton(parent=self.widget)
        all_radio.setText("全部")
        layout.addWidget(all_radio)
        # 默认选中
        all_radio.setChecked(True)
        all_radio.toggled.connect(lambda: self.do_search_task("all"))
        # 任务中
        yes_radio = QtWidgets.QRadioButton(parent=self.widget)
        yes_radio.setText("任务中")
        layout.addWidget(yes_radio)
        yes_radio.toggled.connect(lambda: self.do_search_task("yes"))
        # 无任务
        no_radio = QtWidgets.QRadioButton(parent=self.widget)
        no_radio.setText("无任务")
        layout.addWidget(no_radio)
        no_radio.toggled.connect(lambda: self.do_search_task("no"))
        # 分组
        radio_group = QtWidgets.QButtonGroup(self.widget)
        radio_group.setExclusive(True)
        radio_group.addButton(all_radio)
        radio_group.addButton(yes_radio)
        radio_group.addButton(no_radio)
        # 弹簧
        spacer = QtWidgets.QSpacerItem(40, 20,
                                       QtWidgets.QSizePolicy.Policy.Expanding,
                                       QtWidgets.QSizePolicy.Policy.Minimum
                                       )
        layout.addItem(spacer)

    def do_search_task(self, task):
        self.task = task
        self.set_table_data()

    def table_widget(self):
        """初始化表头"""

        self.table = QtWidgets.QTableWidget(parent=self.widget)
        # 添加斑马纹
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        # 设置表格列数
        self.table.setColumnCount(8)
        # 设置表头
        self.table.setHorizontalHeaderLabels(["设备号", "品牌", "厂商", "Android版本号", "分辨率", "在线状态", "任务状态", "操作"])
        # 设置最小列宽
        self.table.horizontalHeader().setMinimumSectionSize(100)
        self.layout.addWidget(self.table)

    def set_table_data(self):
        # devices = DeviceStore().select(self.online, self.task)
        # devices = DeviceService().select(self.online, self.task)
        devices = DeviceService().select_page(self.page_number, self.items_, self.online, self.task)
        self.table.setRowCount(len(devices))
        self.table.setStyleSheet("""
                  QTableWidget {
                      gridline-color: black;
                      background-color: white;
                  }
                  QHeaderView::section {
                      background-color: lightgray;
                      font-weight: bold;
                      font-size: 14px;
                  }
                  QTableWidget::item {
                      padding: 10px;
                  }
                  QTableWidget::item:selected {
                      background-color: lightblue;
                      color: black;
                  }
              """)
        # 添加数据到表格
        for row, device in enumerate(devices):
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(device.device_id))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(device.brand))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(device.manufacturer))
            self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(device.android_version))
            self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(device.resolution_ratio))
            self.table.setItem(row, 5, QtWidgets.QTableWidgetItem("在线" if device.online_state == 1 else "离线"))
            self.table.setItem(row, 6, QtWidgets.QTableWidgetItem("任务中" if device.task_state == 1 else "无任务"))
            delete_btn = QtWidgets.QPushButton()
            delete_btn.setText("删除")
            delete_btn.setStyleSheet("background:red;color:white;")
            delete_btn.clicked.connect(lambda checked, current=device: self.delete(current.id))

            # 设置按钮固定大小
            delete_btn.setFixedSize(70, 20)

            # 创建一个容器（QWidget）
            widget = QtWidgets.QWidget()

            # 创建一个垂直布局
            v_layout = QtWidgets.QVBoxLayout(widget)
            v_layout.setContentsMargins(0, 0, 0, 0)

            # 创建一个水平布局用于居中按钮
            h_layout = QtWidgets.QHBoxLayout()
            h_layout.setContentsMargins(0, 0, 0, 0)

            # 创建水平spacer以实现水平居中
            spacer_left = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Policy.Expanding,
                                                QtWidgets.QSizePolicy.Policy.Minimum)
            spacer_right = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Policy.Expanding,
                                                 QtWidgets.QSizePolicy.Policy.Minimum)

            # 创建垂直spacer以实现垂直居中
            spacer_top = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Policy.Minimum,
                                               QtWidgets.QSizePolicy.Policy.Expanding)

            spacer_bottom = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Policy.Minimum,
                                                  QtWidgets.QSizePolicy.Policy.Expanding)

            # 创建一个水平布局
            h_layout.addItem(spacer_left)  # 添加左边间距
            h_layout.addWidget(delete_btn)  # 添加按钮
            h_layout.addItem(spacer_right)  # 添加右边间距

            # 将水平布局添加到垂直布局中
            v_layout.addItem(spacer_top)  # 顶部间距
            v_layout.addLayout(h_layout)  # 添加水平布局
            v_layout.addItem(spacer_bottom)  # 底部间距

            self.table.setCellWidget(row, 7, widget)

        # 自动调整列宽以适应内容
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    def delete(self, device_id):
        # DeviceStore().delete(device_id)
        DeviceService().delete(device_id)
        self.set_table_data()

    def page_widget(self):
        self.page_control_widget = QtWidgets.QWidget(parent=self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.page_control_widget.sizePolicy().hasHeightForWidth())
        self.page_control_widget.setSizePolicy(sizePolicy)
        self.page_control_widget.setObjectName("page_control_widget")

        verticalLayout = QtWidgets.QVBoxLayout(self.page_control_widget)
        horizontalLayout = QtWidgets.QHBoxLayout()

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        horizontalLayout.addItem(spacerItem)

        self.p_button = QtWidgets.QPushButton(parent=self.page_control_widget)
        self.p_button.setObjectName("p_button")
        self.p_button.setText("上一页")
        self.p_button.clicked.connect(self.previous_page)
        horizontalLayout.addWidget(self.p_button)

        self.n_button = QtWidgets.QPushButton(parent=self.page_control_widget)
        self.n_button.setObjectName("n_button")
        self.n_button.setText("下一页")
        self.n_button.clicked.connect(self.next_page)
        horizontalLayout.addWidget(self.n_button)

        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        horizontalLayout.addItem(spacerItem1)

        verticalLayout.addLayout(horizontalLayout)

        horizontalLayout_2 = QtWidgets.QHBoxLayout()

        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        horizontalLayout_2.addItem(spacerItem2)

        self.label = QtWidgets.QLabel(parent=self.page_control_widget)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(False)
        self.label.setObjectName("label")
        total_page = DeviceService().select_count_page(self.items_, self.online, self.task)
        self.label.setText(f"共{total_page}页, 当前第1页")
        horizontalLayout_2.addWidget(self.label)

        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        horizontalLayout_2.addItem(spacerItem3)

        verticalLayout.addLayout(horizontalLayout_2)

        self.layout.addWidget(self.page_control_widget)

    def previous_page(self):
        if self.page_number > 0:
            self.page_number -= 1
            self.set_table_data()
            total_pages = DeviceService().select_count_page(online_state=self.online, task_state=self.task, items_=self.items_)
            self.label.setText(f"共{total_pages}页, 当前第{self.page_number+1}页")

    def next_page(self):
        # 1、获取总页数，判断当前页是否为最后一页
        total_pages = DeviceService().select_count_page(online_state=self.online, task_state=self.task, items_=self.items_)
        # 2、当前页不为最后一页，则遍历下一页
        if self.page_number + 1 < total_pages:
            self.page_number += 1
            self.set_table_data()
            self.label.setText(f"共{total_pages}页, 当前第{self.page_number + 1}页")

        # 当前页为最后一页，则继续查询该页
        else:
            pass
