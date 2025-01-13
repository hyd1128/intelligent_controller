#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2025/1/3 15:27
# @Author : limber
# @desc :
import math
from datetime import datetime, time, date
from typing import Any

from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import Qt, QTime, QDate
from PyQt6.QtWidgets import QHBoxLayout, QTableWidgetItem, QWidget, QVBoxLayout, QTableWidget, QHeaderView
from qfluentwidgets import TableWidget, PrimaryPushButton, ComboBox, BodyLabel, MessageBoxBase, LineEdit, ZhDatePicker, \
    TimePicker

from database_service.model.advertising_task_model import AdvertisingTask
from database_service.model.advertising_task_record_model import AdvertisingTaskRecord
from database_service.model.app_model import App
from database_service.service.advertising_task_record_service import AdvertisingTaskRecordService
from database_service.service.advertising_task_service import AdvertisingTaskService
from database_service.service.app_service import AppService
from database_service.service.app_task_record_service import AppTaskRecordService
from window_pyqt.component.general_widget import Widget
from window_pyqt.component.message_widget import MessageWidget
from window_pyqt.component.paging_widget import PagingWidget


class AppTaskRecordTableView(Widget):
    def __init__(self, text: str, parent: Any = None):
        super().__init__(text=text, parent=parent)
        self.tableView = None
        self.paging_widget = PagingWidget(parent=self)
        self.init_table()
        self.init_table_data()
        self.paging_widget.update_page_signal.connect(self.update_page_slot)

    def init_table(self):
        """初始化表头"""
        # setTheme(Theme.DARK)

        # self.hBoxLayout = QHBoxLayout(self)
        self.tableView = TableWidget(self)

        # NOTE: use custom item delegate
        # self.tableView.setItemDelegate(CustomTableItemDelegate(self.tableView))

        # select row on right-click
        self.tableView.setSelectRightClickedRow(True)

        # enable border
        self.tableView.setBorderVisible(True)
        self.tableView.setBorderRadius(8)

        self.tableView.setWordWrap(False)
        self.tableView.setColumnCount(3)
        self.vBoxLayout.setContentsMargins(50, 30, 50, 30)
        self.tableView.verticalHeader().hide()
        self.tableView.setHorizontalHeaderLabels(
            ['关联设备', '关联app任务', '操作'])

        # self.primaryButton1 = PrimaryPushButton('添加广告任务', self)
        # self.primaryButton1.clicked.connect(self.show_add_advertising_task_dialog)
        # self.hBoxLayout = QtWidgets.QHBoxLayout()
        # spacer_item_1 = QtWidgets.QSpacerItem(174, 20, QtWidgets.QSizePolicy.Policy.Expanding,
        #                                       QtWidgets.QSizePolicy.Policy.Minimum)
        # self.hBoxLayout.addWidget(self.primaryButton1)
        # self.hBoxLayout.addSpacerItem(spacer_item_1)
        #
        # self.vBoxLayout.addLayout(self.hBoxLayout)
        self.vBoxLayout.addWidget(self.tableView, 2)
        self.vBoxLayout.addWidget(self.paging_widget)

    def init_table_data(self, page_number: int = 1):
        self.tableView.setRowCount(15)
        total_data_nums = AppTaskRecordService.select_count()
        app_task_record_list_obj = AppTaskRecordService.select_list(page_number, 15)

        self.paging_widget.update_page_amount(math.ceil(total_data_nums / 15))

        # 清空现有数据
        self.tableView.clearContents()

        for i, obj_ in enumerate(app_task_record_list_obj):
            self.tableView.setItem(i, 0, QTableWidgetItem(str(obj_.device.device_id)))
            self.tableView.setItem(i, 1, QTableWidgetItem(str(obj_.app_task.id)))

            detail_btn = QtWidgets.QPushButton("详细")
            detail_btn.setStyleSheet("background-color: green; color: black;")
            detail_btn.clicked.connect(
                lambda checked, current=obj_: self.show_detail_app_task_record_dialog(obj_=current))
            delete_btn = QtWidgets.QPushButton("删除")
            delete_btn.setStyleSheet("background-color: red; color: black;")
            delete_btn.clicked.connect(lambda checked, current=obj_: self.delete_app_task_record(current.id))

            # 创建一个容器和布局
            widget = QtWidgets.QWidget()
            layout = QtWidgets.QHBoxLayout(widget)
            layout.setSpacing(5)
            layout.setContentsMargins(0, 0, 0, 0)

            # 添加上下左右的弹性空白并居中按钮
            layout.addStretch()  # 左边弹性
            layout.addWidget(detail_btn)  # 居中按钮
            layout.addWidget(delete_btn)  # 居中按钮
            layout.addStretch()  # 右边弹性

            self.tableView.setCellWidget(i, 2, widget)

        # 设置表格不可编辑
        self.tableView.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tableView.resizeColumnsToContents()
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tableView.setSortingEnabled(True)
        self.setStyleSheet("Demo{background: rgb(255, 255, 255)} ")

    def delete_app_task_record(self, app_id):
        # 删除数据
        result = AppTaskRecordService.delete(app_id)
        if result:
            # # 立即重新加载当前页数据
            # current_page = self.paging_widget.page_number_
            # self.tableView.clearContents()  # 清空当前表格内容
            # self.init_table_data(current_page)  # 重新加载数据
            self.update_page()

    def update_page_slot(self, page_number):
        self.tableView.clearContents()  # 清空当前表格内容
        self.init_table_data(page_number)

    def show_detail_app_task_record_dialog(self, obj_):
        w = DetailAdvertisingTaskRecordDialog(self, obj_=obj_)
        if w.exec():
            pass
        else:
            pass

    def update_page(self):
        current_page = self.paging_widget.page_number_
        self.tableView.clearContents()  # 清空当前表格内容
        self.init_table_data(current_page)  # 重新加载数据


class DetailAdvertisingTaskRecordDialog(MessageBoxBase):
    """ Custom message box """

    def __init__(self, parent=None, obj_=None):
        super().__init__(parent)
        # self.resize(1000, 600)
        vbox1 = QVBoxLayout()
        vbox2 = QVBoxLayout()
        hbox1 = QHBoxLayout()

        self.device_label = BodyLabel('关联设备: ', self)
        self.app_task_label = BodyLabel('关联app任务: ', self)

        vbox1.addWidget(self.device_label)
        vbox1.addWidget(self.app_task_label)

        ###############################

        self.device_label = LineEdit(self)
        self.app_task_label = LineEdit(self)

        self.device_label.setText(str(obj_.device.device_id))
        self.app_task_label.setText(str(obj_.app_task.id))

        vbox2.addWidget(self.device_label)
        vbox2.addWidget(self.app_task_label)

        hbox1.addLayout(vbox1)
        hbox1.addLayout(vbox2)

        self.viewLayout.addLayout(hbox1)

        # change the text of button
        self.yesButton.setText('确定')
        self.cancelButton.setText('取消')

        self.widget.setMinimumWidth(500)

    def validate(self) -> bool:
        return True








