from PyQt6 import QtWidgets, QtCore
from window.dialog.save_app import SaveAppDialog
from store_service.service.service_app import AppService


class AppPage:
    def __init__(self, parent):
        self.__parent = parent
        self.setup()

    def setup(self):
        # 加入父组件
        self.widget = QtWidgets.QWidget()
        self.__parent.widget.addWidget(self.widget)
        # 布局
        self.layout = QtWidgets.QVBoxLayout(self.widget)

        # 引入子组件
        self.add_btn()
        self.table_widget()

        # 初始化数据
        self.set_table_data()

        # 添加按钮界面
        self.page_widget()

    # 添加按钮
    def add_btn(self):
        # 布局
        layout = QtWidgets.QHBoxLayout()
        # 弹簧
        spacer = QtWidgets.QSpacerItem(40, 20,
                                       QtWidgets.QSizePolicy.Policy.Expanding,
                                       QtWidgets.QSizePolicy.Policy.Minimum
                                       )
        layout.addItem(spacer)
        # 按钮
        btn = QtWidgets.QPushButton(parent=self.widget)
        btn.setText("添加应用")
        btn.clicked.connect(lambda: self.save_dialog())
        layout.addWidget(btn)
        self.layout.addLayout(layout)

    # 列表
    def table_widget(self):
        self.table = QtWidgets.QTableWidget(parent=self.widget)

        # 添加斑马纹
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)

        # 设置表格列数
        self.table.setColumnCount(3)

        # 设置表头
        self.table.setHorizontalHeaderLabels(["包名", "名称", "操作"])

        # 设置最小列宽
        self.table.horizontalHeader().setMinimumSectionSize(100)

        self.layout.addWidget(self.table)

    def set_table_data(self):
        # apps = AppStore().select()
        apps = AppService().select()
        self.table.setRowCount(len(apps))
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
        for row, app in enumerate(apps):
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(app.app))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(app.app))
            delete_btn = QtWidgets.QPushButton()
            delete_btn.setText("删除")
            delete_btn.setStyleSheet("background:red;color:white;")
            delete_btn.clicked.connect(lambda checked, current=app: self.delete(current.app))

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

            self.table.setCellWidget(row, 2, widget)
            # 自动调整列宽以适应内容
            self.table.resizeColumnsToContents()
            self.table.resizeRowsToContents()

    # 添加应用
    def save_dialog(self, app=None):
        if app is None:
            app = {
                "name": "",
                "package_name": ""
            }
        SaveAppDialog(app, self).exec()

    # 删除应用
    def delete(self, app_name):
        # AppStore().delete(package_name)
        AppService().delete_by_name(app_name)
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
        self.label.setText("共1页, 当前第1页")
        horizontalLayout_2.addWidget(self.label)

        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        horizontalLayout_2.addItem(spacerItem3)

        verticalLayout.addLayout(horizontalLayout_2)

        self.layout.addWidget(self.page_control_widget)

    def previous_page(self):
        print("上一页")
        self.label.setText("共1页, 当前第1页")

    def next_page(self):
        print("下一页")
        self.label.setText("共1页, 当前第1页")
