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
    TimePicker, PlainTextEdit

from database_service.model.advertising_task_model import AdvertisingTask
from database_service.model.app_model import App
from database_service.model.script_model import Script
from database_service.service.advertising_task_service import AdvertisingTaskService
from database_service.service.app_service import AppService
from database_service.service.script_service import ScriptService
from window_pyqt.component.general_widget import Widget
from window_pyqt.component.message_widget import MessageWidget
from window_pyqt.component.paging_widget import PagingWidget


class ScriptTableView(Widget):
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
            ['脚本名称', '关联app', '操作'])

        self.primaryButton1 = PrimaryPushButton('添加脚本', self)
        self.primaryButton1.clicked.connect(self.show_add_script_dialog)
        self.hBoxLayout = QtWidgets.QHBoxLayout()
        spacer_item_1 = QtWidgets.QSpacerItem(174, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                              QtWidgets.QSizePolicy.Policy.Minimum)
        self.hBoxLayout.addWidget(self.primaryButton1)
        self.hBoxLayout.addSpacerItem(spacer_item_1)

        self.vBoxLayout.addLayout(self.hBoxLayout)
        self.vBoxLayout.addWidget(self.tableView, 2)
        self.vBoxLayout.addWidget(self.paging_widget)

    def init_table_data(self, page_number: int = 1):
        self.tableView.setRowCount(15)
        total_data_nums = ScriptService.select_count()
        script_list_obj = ScriptService.select_list(page_number, 15)

        self.paging_widget.update_page_amount(math.ceil(total_data_nums / 15))

        # 清空现有数据
        self.tableView.clearContents()

        for i, obj_ in enumerate(script_list_obj):
            self.tableView.setItem(i, 0, QTableWidgetItem(obj_.script_name))
            self.tableView.setItem(i, 1, QTableWidgetItem(str(obj_.app.app_name)))

            detail_btn = QtWidgets.QPushButton("详细")
            detail_btn.setStyleSheet("background-color: green; color: black;")
            detail_btn.clicked.connect(
                lambda checked, current=obj_: self.show_detail_script_dialog(obj_=current))
            delete_btn = QtWidgets.QPushButton("删除")
            delete_btn.setStyleSheet("background-color: red; color: black;")
            delete_btn.clicked.connect(lambda checked, current=obj_: self.delete_script(current.id))

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

    def delete_script(self, script_id):
        # 删除数据
        result = ScriptService.delete(script_id)
        if result:
            # # 立即重新加载当前页数据
            # current_page = self.paging_widget.page_number_
            # self.tableView.clearContents()  # 清空当前表格内容
            # self.init_table_data(current_page)  # 重新加载数据
            self.update_page()

    def update_page_slot(self, page_number):
        self.tableView.clearContents()  # 清空当前表格内容
        self.init_table_data(page_number)

    def show_add_script_dialog(self):
        w = AddScriptDialog(self)
        if w.exec():
            MessageWidget.success_message(self, content="添加成功")
        else:
            MessageWidget.error_message(self, content="添加失败")

    def show_detail_script_dialog(self, obj_):
        w = DetailScriptDialog(self, obj_=obj_)
        if w.exec():
            pass
        else:
            pass

    def update_page(self):
        current_page = self.paging_widget.page_number_
        self.tableView.clearContents()  # 清空当前表格内容
        self.init_table_data(current_page)  # 重新加载数据


class AddScriptDialog(MessageBoxBase):
    """ Custom message box """

    def __init__(self, parent=None):
        super().__init__(parent)
        # self.resize(1000, 600)
        vbox1 = QVBoxLayout()
        vbox2 = QVBoxLayout()
        hbox1 = QHBoxLayout()

        self.script_name_label = BodyLabel('脚本名称: ', self)
        self.script_content_label = BodyLabel('脚本内容: ', self)
        self.script_type_label = BodyLabel('脚本类型: ', self)
        self.app_label = BodyLabel('关联app: ', self)

        vbox1.addWidget(self.script_name_label)
        vbox1.addWidget(self.script_content_label)
        vbox1.addWidget(self.script_type_label)
        vbox1.addWidget(self.app_label)

        self.script_name_edit = LineEdit(self)
        self.script_content_edit = PlainTextEdit(self)
        self.script_content_edit.setFixedSize(500, 110)
        self.script_type_edit = RadioButtonWidget()
        self.app_edit = AppRadioButtonWidget()

        vbox2.addWidget(self.script_name_edit)
        vbox2.addWidget(self.script_content_edit)
        vbox2.addWidget(self.script_type_edit)
        vbox2.addWidget(self.app_edit)

        hbox1.addLayout(vbox1)
        hbox1.addLayout(vbox2)

        self.script_name_edit.setClearButtonEnabled(True)
        # self.script_content_edit.setClearButtonEnabled(True)

        self.viewLayout.addLayout(hbox1)

        # change the text of button
        self.yesButton.setText('添加')
        self.cancelButton.setText('取消')

        self.widget.setMinimumWidth(500)

    def validate(self) -> bool:
        script_ = Script(
            script_name=self.script_name_edit.text(),
            script_content=self.script_content_edit.toPlainText(),
            script_type=self.script_type_edit.get_selected_method(),
            app=self.app_edit.get_selected_method()
        )

        ScriptService.add(script_)
        return True


class DetailScriptDialog(MessageBoxBase):
    """ Custom message box """

    def __init__(self, parent=None, obj_=None):
        super().__init__(parent)
        # self.resize(1000, 600)
        vbox1 = QVBoxLayout()
        vbox2 = QVBoxLayout()
        hbox1 = QHBoxLayout()

        self.script_name_label = BodyLabel('脚本名称: ', self)
        self.script_content_label = BodyLabel('脚本内容: ', self)
        self.script_type_label = BodyLabel('脚本类型: ', self)
        self.app_label = BodyLabel('关联app: ', self)

        vbox1.addWidget(self.script_name_label)
        vbox1.addWidget(self.script_content_label)
        vbox1.addWidget(self.script_type_label)
        vbox1.addWidget(self.app_label)

        self.script_name_edit = LineEdit(self)
        self.script_content_edit = PlainTextEdit(self)
        self.script_content_edit.setFixedSize(500, 110)
        self.script_type_edit = LineEdit(self)
        self.app_edit = LineEdit(self)

        vbox2.addWidget(self.script_name_edit)
        vbox2.addWidget(self.script_content_edit)
        vbox2.addWidget(self.script_type_edit)
        vbox2.addWidget(self.app_edit)

        self.script_name_edit.setText(obj_.script_name)
        self.script_content_edit.setPlainText(obj_.script_content)
        self.script_type_edit.setText(obj_.script_type)
        self.app_edit.setText(obj_.app.app_name)

        self.script_name_edit.setReadOnly(True)
        self.script_content_edit.setReadOnly(True)
        self.script_type_edit.setReadOnly(True)
        self.app_edit.setReadOnly(True)

        hbox1.addLayout(vbox1)
        hbox1.addLayout(vbox2)

        self.script_name_edit.setClearButtonEnabled(True)
        # self.script_content_edit.setClearButtonEnabled(True)

        self.viewLayout.addLayout(hbox1)

        # change the text of button
        self.yesButton.setText('确定')
        self.cancelButton.setText('取消')

        self.widget.setMinimumWidth(500)

    def validate(self) -> bool:
        return True


class RadioButtonWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 添加布局
        layout = QVBoxLayout(self)

        self.comboBox = ComboBox(self)
        self.comboBox.setPlaceholderText("选择脚本类型")

        items = ['app', 'advertising']
        self.comboBox.addItems(items)
        self.comboBox.setCurrentIndex(-1)
        self.comboBox.currentTextChanged.connect(print)

        # 将 ComboBox 添加到布局中
        layout.addWidget(self.comboBox)
        layout.setContentsMargins(0, 0, 0, 0)  # 设置边距为0

    def get_selected_method(self) -> str:
        """获取选择的下载方式"""
        return self.comboBox.currentText()


class AppRadioButtonWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 添加布局
        layout = QVBoxLayout(self)

        self.comboBox = ComboBox(self)
        self.comboBox.setPlaceholderText("选择下载方式")

        app_list = AppService.select_all()
        app_name_list = [app_.app_name for app_ in app_list]
        self.comboBox.addItems(app_name_list)
        self.comboBox.setCurrentIndex(-1)
        self.comboBox.currentTextChanged.connect(print)

        # 将 ComboBox 添加到布局中
        layout.addWidget(self.comboBox)
        layout.setContentsMargins(0, 0, 0, 0)  # 设置边距为0

    def get_selected_method(self) -> str:
        """获取选择的下载方式"""
        app_name = self.comboBox.currentText()
        app_ = AppService.select_by_name(app_name)
        return app_
