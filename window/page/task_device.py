from PyQt6 import QtWidgets, QtCore
from store_service.service.service_record import RecordService


class TaskDevicePage:
    def __init__(self, parent):
        self.__parent = parent
        # 定义单页展示的记录条数
        self.per_page_item = 15
        # 定义默认页码
        self.page_number = 0
        self.setup()


    def setup(self):
        # 加入父组件
        self.widget = QtWidgets.QWidget()
        self.__parent.widget.addWidget(self.widget)
        # 布局
        self.layout = QtWidgets.QVBoxLayout(self.widget)

        # 引入子组件
        self.table_widget()

        # 初始化数据
        self.set_table_data()

        # 引入按钮主键
        self.page_btn_widget()

        # 引入页码
        self.page_widget()

    # 列表
    def table_widget(self):
        self.table = QtWidgets.QTableWidget(parent=self.widget)
        # 添加斑马纹
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        # 设置表格列数
        self.table.setColumnCount(8)
        # 设置表头
        self.table.setHorizontalHeaderLabels(["设备ID",
                                              "任务名",
                                              "已执行次数",
                                              "任务开始运行时间",
                                              "任务结束运行时间",
                                              "最大执行次数",
                                              "最新执行时间",
                                              "日期"
                                              ])

        # 设置最小列宽
        self.table.horizontalHeader().setMinimumSectionSize(100)

        self.layout.addWidget(self.table)

    def set_table_data(self, per_page_item: int = 15, page_numbers: int = 0):
        # task_devices = TaskDeviceStore().select()
        # task_devices = RecordService().select_all()
        task_devices = RecordService().select_page_data(per_page_item, page_numbers)
        self.table.setRowCount(len(task_devices))
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
        for row, task_device in enumerate(task_devices):
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(task_device.device_id))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(f'{task_device.task_name}'))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(f'{task_device.execution_times}'))
            self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(f'{task_device.today_execution_time}'))
            self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(f'{task_device.today_end_execution_time}'))
            self.table.setItem(row, 5, QtWidgets.QTableWidgetItem(f'{task_device.specify_device_execution_times}'))
            self.table.setItem(row, 6, QtWidgets.QTableWidgetItem(f'{task_device.task_last_execution_time}'))
            self.table.setItem(row, 7, QtWidgets.QTableWidgetItem(f'{task_device.date}'))

            # 自动调整列宽以适应内容
            self.table.resizeColumnsToContents()
            self.table.resizeRowsToContents()

    def page_btn_widget(self):
        self.widget_btn = QtWidgets.QWidget(parent=self.widget)
        self.widget_btn.setObjectName("widget_btn")

        horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_btn)
        horizontalLayout_2.setSpacing(20)
        horizontalLayout_2.setObjectName("horizontalLayout_2")

        spacerItem = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Minimum)
        horizontalLayout_2.addItem(spacerItem)

        self.p_page_btn = QtWidgets.QPushButton(parent=self.widget_btn)
        self.p_page_btn.setObjectName("p_page_btn")
        self.p_page_btn.setText("上一页")
        # 绑定槽函数
        self.p_page_btn.clicked.connect(self.p_page)
        horizontalLayout_2.addWidget(self.p_page_btn)

        self.n_page_btn = QtWidgets.QPushButton(parent=self.widget_btn)
        self.n_page_btn.setObjectName("n_page_btn")
        self.n_page_btn.setText("下一页")
        # 绑定槽函数
        self.n_page_btn.clicked.connect(self.n_page)
        horizontalLayout_2.addWidget(self.n_page_btn)

        spacerItem1 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                            QtWidgets.QSizePolicy.Policy.Minimum)
        horizontalLayout_2.addItem(spacerItem1)

        self.layout.addWidget(self.widget_btn)

    def page_widget(self):
        self.page_number_widget = QtWidgets.QWidget(parent=self.widget)
        self.page_number_widget.setObjectName("page_number_widget")

        horizontalLayout = QtWidgets.QHBoxLayout(self.page_number_widget)

        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Minimum)
        horizontalLayout.addItem(spacerItem)

        self.page_number_label = QtWidgets.QLabel(parent=self.page_number_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.page_number_label.sizePolicy().hasHeightForWidth())
        self.page_number_label.setSizePolicy(sizePolicy)
        self.page_number_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom | QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.page_number_label.setWordWrap(False)
        total_pages = RecordService().get_total_page(self.per_page_item)
        self.page_number_label.setText(f"共{total_pages}页, 当前第1页")
        horizontalLayout.addWidget(self.page_number_label)

        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                            QtWidgets.QSizePolicy.Policy.Minimum)
        horizontalLayout.addItem(spacerItem1)
        self.layout.addWidget(self.page_number_widget)

    def p_page(self):
        # 1、当前页是否为第一页，如果为第一页，点击按钮后继续显示该页
        # 2、当前页如果不为第一页，则显示上一页数据
        if self.page_number > 0:
            self.page_number -= 1
            self.set_table_data(page_numbers=self.page_number)
            total_pages = RecordService().get_total_page(self.per_page_item)
            self.page_number_label.setText(f"共{total_pages}页, 当前第{self.page_number+1}页")

    def n_page(self):
        # 1、获取总页数，判断当前页是否为最后一页
        total_pages = RecordService().get_total_page(self.per_page_item)
        # 2、当前页不为最后一页，则遍历下一页
        if self.page_number + 1 < total_pages:
            self.page_number += 1
            self.set_table_data(page_numbers=self.page_number)
            self.page_number_label.setText(f"共{total_pages}页, 当前第{self.page_number+1}页")

        # 当前页为最后一页，则继续查询该页
        else:
            pass








