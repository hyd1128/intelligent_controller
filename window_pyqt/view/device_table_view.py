#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2025/1/3 15:27
# @Author : limber
# @desc :
import math
from typing import Any

from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QTableWidgetItem, QWidget, QVBoxLayout, QTableWidget, QHeaderView
from qfluentwidgets import TableWidget, PrimaryPushButton, ComboBox, BodyLabel, MessageBoxBase, LineEdit

from database_service.model.device_model import Device
from database_service.service.device_service import DeviceService
from window_pyqt.component.general_widget import Widget
from window_pyqt.component.paging_widget import PagingWidget


class DeviceTableView(Widget):
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

        # 设置列数
        self.tableView.setColumnCount(5)
        self.vBoxLayout.setContentsMargins(50, 30, 50, 30)
        self.tableView.verticalHeader().hide()
        self.tableView.setHorizontalHeaderLabels(
            ['设备ID', '设备品牌', '连接状态', '任务状态', 'operation'])

        self.vBoxLayout.addWidget(self.tableView, 2)
        self.vBoxLayout.addWidget(self.paging_widget)

    def init_table_data(self, page_number: int = 1):
        self.tableView.setRowCount(15)
        total_data_nums = DeviceService.select_count()
        device_list_obj = DeviceService.select_list(page_number, 15)

        self.paging_widget.update_page_amount(math.ceil(total_data_nums / 15))

        # 清空现有数据
        self.tableView.clearContents()

        for i, obj_ in enumerate(device_list_obj):
            self.tableView.setItem(i, 0, QTableWidgetItem(obj_.device_id))
            self.tableView.setItem(i, 1, QTableWidgetItem(obj_.brand))
            if int(obj_.online_state) == 1:
                online_ = "在线"
            else:
                online_ = "离线"
            self.tableView.setItem(i, 2, QTableWidgetItem(online_))
            if int(obj_.task_state) == 1:
                task_ = "任务中"
            else:
                task_ = "无任务"
            self.tableView.setItem(i, 3, QTableWidgetItem(task_))

            detail_btn = QtWidgets.QPushButton("详细")
            detail_btn.setStyleSheet("background-color: green; color: black;")
            detail_btn.clicked.connect(lambda checked, current=obj_: self.show_detail_device_dialog(obj_=current))
            delete_btn = QtWidgets.QPushButton("删除")
            delete_btn.setStyleSheet("background-color: red; color: black;")
            delete_btn.clicked.connect(lambda checked, current=obj_: self.delete_device(current.id))

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

            self.tableView.setCellWidget(i, 4, widget)

        # 设置表格不可编辑
        self.tableView.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tableView.resizeColumnsToContents()
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tableView.setSortingEnabled(True)
        self.setStyleSheet("Demo{background: rgb(255, 255, 255)} ")

    def delete_device(self, device_id):
        # 删除数据
        result = DeviceService.delete_device(device_id)
        if result:
            # # 立即重新加载当前页数据
            # current_page = self.paging_widget.page_number_
            # self.tableView.clearContents()  # 清空当前表格内容
            # self.init_table_data(current_page)  # 重新加载数据

            self.update_page()

    def update_page_slot(self, page_number):
        self.tableView.clearContents()  # 清空当前表格内容
        self.init_table_data(page_number)

    def show_detail_device_dialog(self, obj_):
        w = DetailDeviceDialog(self, obj_=obj_)
        if w.exec():
            pass
        else:
            pass

    def update_page(self):
        current_page = self.paging_widget.page_number_
        self.tableView.clearContents()  # 清空当前表格内容
        self.init_table_data(current_page)  # 重新加载数据


class DetailDeviceDialog(MessageBoxBase):
    """ Custom message box """

    def __init__(self, parent=None, obj_: Device = None):
        super().__init__(parent)
        # self.resize(1000, 600)
        vbox1 = QVBoxLayout()
        vbox2 = QVBoxLayout()
        hbox1 = QHBoxLayout()

        self.device_label = BodyLabel('设备ID: ', self)
        self.brand_label = BodyLabel('品牌: ', self)
        self.manufacturer_label = BodyLabel('厂商: ', self)
        self.resolution_ration = BodyLabel('分辨率: ', self)
        self.online_state_label = BodyLabel('在线状态: ', self)
        self.task_state_label = BodyLabel('任务状态: ', self)
        self.locating_app_status_label = BodyLabel('定位app状态: ', self)
        self.locating_app_last_reload_time_label = BodyLabel('定位app上一次重启时间: ', self)
        self.download_app_package_name_label = BodyLabel('已下载app包名: ', self)

        vbox1.addWidget(self.device_label)
        vbox1.addWidget(self.brand_label)
        vbox1.addWidget(self.manufacturer_label)
        vbox1.addWidget(self.resolution_ration)
        vbox1.addWidget(self.online_state_label)
        vbox1.addWidget(self.task_state_label)
        vbox1.addWidget(self.locating_app_status_label)
        vbox1.addWidget(self.locating_app_last_reload_time_label)
        vbox1.addWidget(self.download_app_package_name_label)

        self.device_edit = LineEdit(self)
        self.brand_edit = LineEdit(self)
        self.manufacturer_edit = LineEdit(self)
        self.resolution_edit = LineEdit(self)
        self.online_state_edit = LineEdit(self)
        self.task_state_edit = LineEdit(self)
        self.locating_app_status_edit = LineEdit(self)
        self.locating_app_last_reload_time_edit = LineEdit(self)
        self.download_app_package_name_edit = LineEdit(self)

        self.device_edit.setText(obj_.device_id)
        self.brand_edit.setText(obj_.brand)
        self.manufacturer_edit.setText(obj_.manufacturer)
        self.resolution_edit.setText(obj_.resolution_ration)
        self.online_state_edit.setText("在线" if int(obj_.online_state) == 1 else "离线")
        self.task_state_edit.setText("任务中" if int(obj_.task_state) == 1 else "无任务")
        self.locating_app_status_edit.setText("开启" if int(obj_.locating_app_status) else "关闭")
        self.locating_app_last_reload_time_edit.setText(str(obj_.locating_app_last_reload_time))
        self.download_app_package_name_edit.setText(obj_.download_app)

        self.device_edit.setReadOnly(True)
        self.brand_edit.setReadOnly(True)
        self.manufacturer_edit.setReadOnly(True)
        self.resolution_edit.setReadOnly(True)
        self.online_state_edit.setReadOnly(True)
        self.task_state_edit.setReadOnly(True)
        self.locating_app_status_edit.setReadOnly(True)
        self.locating_app_last_reload_time_edit.setReadOnly(True)
        self.download_app_package_name_edit.setReadOnly(True)

        vbox2.addWidget(self.device_edit)
        vbox2.addWidget(self.brand_edit)
        vbox2.addWidget(self.manufacturer_edit)
        vbox2.addWidget(self.resolution_edit)
        vbox2.addWidget(self.online_state_edit)
        vbox2.addWidget(self.task_state_edit)
        vbox2.addWidget(self.locating_app_status_edit)
        vbox2.addWidget(self.locating_app_last_reload_time_edit)
        vbox2.addWidget(self.download_app_package_name_edit)

        hbox1.addLayout(vbox1)
        hbox1.addLayout(vbox2)

        self.viewLayout.addLayout(hbox1)

        # change the text of button
        self.yesButton.setText('确定')
        self.yesButton.disconnect()
        self.yesButton.clicked.connect(self.validate_detail)
        self.cancelButton.setText('关闭')

        self.widget.setMinimumWidth(500)

    def validate_detail(self):
        self.accept()
