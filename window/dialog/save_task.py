from PyQt6 import QtWidgets
from PyQt6.QtCore import QTime
from PyQt6.QtWidgets import QVBoxLayout, QDialog, QLabel, QPushButton, QHBoxLayout, QLineEdit, QFileDialog, QTimeEdit

from store_service.service.service_task import TaskService
from store_service.model.model_task import Task

class SaveTaskDialog(QDialog):

    def __init__(self, task, parent):
        super().__init__()
        self.task = task
        self.__parent = parent

        self.setWindowTitle('应用编辑')
        self.resize(500, 200)

        # label
        # 任务label
        name_key = QLabel()
        name_key.setText("任务名")
        # 包名label
        package_key = QLabel()
        package_key.setText("应用包名")
        # 任务持续执行时间
        task_execution_duration_label = QLabel("任务持续执行时长")
        # 最少执行次数label
        min_tims_label = QLabel()
        min_tims_label.setText("最少执行次数")
        # 最多执行次数label
        max_times_label = QLabel()
        max_times_label.setText("最多执行次数")
        # 任务发布日期label
        date_label = QLabel()
        date_label.setText("任务发布日期")
        # label layout
        label_layout = QVBoxLayout()
        label_layout.addWidget(name_key)
        label_layout.addWidget(package_key)
        label_layout.addWidget(task_execution_duration_label)
        label_layout.addWidget(min_tims_label)
        label_layout.addWidget(max_times_label)
        label_layout.addWidget(date_label)

        # edit
        # name
        self.name_val = QLineEdit()
        self.name_val.setPlaceholderText("请输入任务名")
        self.name_val.setText(self.task["name"])
        # package
        self.package_val = QLineEdit()
        self.package_val.setPlaceholderText("请输入应用包名")
        self.package_val.setText(task["package_name"])
        # 任务持续执行时间
        self.time_edit = QTimeEdit(QTime.currentTime())
        self.time_edit.setDisplayFormat('HH:mm:ss')
        self.time_edit.setTimeRange(QTime(0, 0, 0), QTime(24, 60, 60))
        # 最少执行次数
        self.min_times_edit = QLineEdit()
        self.min_times_edit.setPlaceholderText("请输入")
        self.min_times_edit.setText(task["minimum_execution_times"])
        # 最多执行次数
        self.max_times_edit = QLineEdit()
        self.max_times_edit.setPlaceholderText("请输入")
        self.max_times_edit.setText(self.task["maximum_execution_times"])
        # 任务发布日期
        self.date_edit = QLineEdit()
        self.date_edit.setPlaceholderText("请输入")
        self.date_edit.setText(task["task_release_time"])
        # edit layout
        edit_layout = QVBoxLayout()
        edit_layout.addWidget(self.name_val)
        edit_layout.addWidget(self.package_val)
        edit_layout.addWidget(self.time_edit)
        edit_layout.addWidget(self.min_times_edit)
        edit_layout.addWidget(self.max_times_edit)
        edit_layout.addWidget(self.date_edit)

        # label edit layout
        label_edit_layout = QHBoxLayout()
        label_edit_layout.addLayout(label_layout)
        label_edit_layout.addLayout(edit_layout, stretch=1)

        # 按钮
        # button
        button_layout = QHBoxLayout()
        spacer_left = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Policy.Expanding,
                                            QtWidgets.QSizePolicy.Policy.Minimum)
        spacer_right = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Policy.Expanding,
                                             QtWidgets.QSizePolicy.Policy.Minimum)
        # 保存按钮
        save_btn = QPushButton()
        save_btn.setText("保存")
        save_btn.clicked.connect(self.save)
        button_layout.addItem(spacer_left)
        button_layout.addWidget(save_btn)
        button_layout.addItem(spacer_right)

        # 整体布局
        self.layout = QVBoxLayout(self)
        self.layout.addLayout(label_edit_layout)
        self.layout.addLayout(button_layout)

    def save(self):
        task_ = Task(task_name=self.name_val.text(),
                     app=self.package_val.text(),
                     task_execution_duration=self.time_edit.text(),
                     min_execution_times=self.min_times_edit.text(),
                     max_execution_times=self.max_times_edit.text(),
                     task_release_date=self.date_edit.text())
        TaskService().add_task(task_)

        # task = {
        #     "name": self.name_val.text(),
        #     "package_name": self.package_val.text(),
        #     "task_execution_duration": self.time_edit.text(),
        #     "minimum_execution_times": self.min_times_edit.text(),
        #     "maximum_execution_times": self.max_times_edit.text(),
        #     "task_release_time": self.date_edit.text(),
        # }
        #
        # TaskStore().add(task)
        self.__parent.set_table_data()
        self.accept()
