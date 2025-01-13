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

from database_service.model.app_model import App
from database_service.service.app_service import AppService
from window_pyqt.component.general_widget import Widget
from window_pyqt.component.message_widget import MessageWidget
from window_pyqt.component.paging_widget import PagingWidget


class AppTableView(Widget):
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
        self.tableView.setColumnCount(6)
        self.vBoxLayout.setContentsMargins(50, 30, 50, 30)
        self.tableView.verticalHeader().hide()
        self.tableView.setHorizontalHeaderLabels(
            ['应用名称', '包名', '版本号', '下载连接', '下载方法', '操作'])

        self.primaryButton1 = PrimaryPushButton('添加应用', self)
        self.primaryButton1.clicked.connect(self.show_add_app_dialog)
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
        total_data_nums = AppService.select_count()
        app_list_obj = AppService.select_list(page_number, 15)

        self.paging_widget.update_page_amount(math.ceil(total_data_nums / 15))

        # 清空现有数据
        self.tableView.clearContents()

        for i, obj_ in enumerate(app_list_obj):
            self.tableView.setItem(i, 0, QTableWidgetItem(obj_.app_name))
            self.tableView.setItem(i, 1, QTableWidgetItem(obj_.package_name))
            self.tableView.setItem(i, 2, QTableWidgetItem(obj_.version))
            self.tableView.setItem(i, 3, QTableWidgetItem(obj_.download_link))
            self.tableView.setItem(i, 4, QTableWidgetItem(obj_.download_method))

            detail_btn = QtWidgets.QPushButton("详细")
            detail_btn.setStyleSheet("background-color: green; color: black;")
            detail_btn.clicked.connect(lambda checked, current=obj_: self.show_detail_app_dialog(obj_=current))
            delete_btn = QtWidgets.QPushButton("删除")
            delete_btn.setStyleSheet("background-color: red; color: black;")
            delete_btn.clicked.connect(lambda checked, current=obj_: self.delete_app(current.id))

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

            self.tableView.setCellWidget(i, 5, widget)

        # 设置表格不可编辑
        self.tableView.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tableView.resizeColumnsToContents()
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tableView.setSortingEnabled(True)
        self.setStyleSheet("Demo{background: rgb(255, 255, 255)} ")

    def delete_app(self, app_id):
        # 删除数据
        result = AppService.delete_app(app_id)
        if result:
            # # 立即重新加载当前页数据
            # current_page = self.paging_widget.page_number_
            # self.tableView.clearContents()  # 清空当前表格内容
            # self.init_table_data(current_page)  # 重新加载数据
            self.update_page()

    def update_page_slot(self, page_number):
        self.tableView.clearContents()  # 清空当前表格内容
        self.init_table_data(page_number)

    def show_add_app_dialog(self):
        w = AddAppDialog(self)
        if w.exec():
            MessageWidget.success_message(self, content="添加成功")
        else:
            MessageWidget.error_message(self, content="添加失败")
        self.update_page()

    def show_detail_app_dialog(self, obj_):
        w = DetailAppDialog(self, obj_=obj_)
        if w.exec():
            pass
        else:
            pass

    def update_page(self):
        current_page = self.paging_widget.page_number_
        self.tableView.clearContents()  # 清空当前表格内容
        self.init_table_data(current_page)  # 重新加载数据


class AddAppDialog(MessageBoxBase):
    """ Custom message box """

    def __init__(self, parent=None):
        super().__init__(parent)
        # self.resize(1000, 600)
        vbox1 = QVBoxLayout()
        vbox2 = QVBoxLayout()
        hbox1 = QHBoxLayout()

        self.app_name_label = BodyLabel('app名称: ', self)
        self.app_package_label = BodyLabel('app包名: ', self)
        self.app_version_label = BodyLabel('app版本: ', self)
        self.download_url_label = BodyLabel('下载短链接: ', self)
        self.download_method_label = BodyLabel('下载方式: ', self)

        vbox1.addWidget(self.app_name_label)
        vbox1.addWidget(self.app_package_label)
        vbox1.addWidget(self.app_version_label)
        vbox1.addWidget(self.download_url_label)
        vbox1.addWidget(self.download_method_label)

        self.app_name_edit = LineEdit(self)
        self.app_package_edit = LineEdit(self)
        self.app_version_edit = LineEdit(self)
        self.download_url_edit = LineEdit(self)
        self.download_method_edit = RadioButtonWidget()

        vbox2.addWidget(self.app_name_edit)
        vbox2.addWidget(self.app_package_edit)
        vbox2.addWidget(self.app_version_edit)
        vbox2.addWidget(self.download_url_edit)
        vbox2.addWidget(self.download_method_edit)

        hbox1.addLayout(vbox1)
        hbox1.addLayout(vbox2)

        self.app_name_edit.setClearButtonEnabled(True)
        self.app_package_edit.setClearButtonEnabled(True)
        self.app_version_edit.setClearButtonEnabled(True)
        self.download_url_edit.setClearButtonEnabled(True)

        self.viewLayout.addLayout(hbox1)

        # change the text of button
        self.yesButton.setText('添加app')
        self.cancelButton.setText('取消')

        self.widget.setMinimumWidth(500)

    def validate(self):
        """重写dialog框的yes验证程序"""
        app = App(
            app_name=self.app_name_edit.text().strip(),
            package_name=self.app_package_edit.text().strip(),
            version=self.app_version_edit.text().strip(),
            download_link=self.download_url_edit.text().strip(),
            download_method=self.download_method_edit.get_selected_method()
        )
        AppService.add(app)
        # MessageWidget.success_message(self, f"添加 {self.app_name_edit.text().strip()}成功")
        return True


class DetailAppDialog(MessageBoxBase):
    """ Custom message box """

    def __init__(self, parent=None, obj_: App = None):
        super().__init__(parent)
        # self.resize(1000, 600)
        vbox1 = QVBoxLayout()
        vbox2 = QVBoxLayout()
        hbox1 = QHBoxLayout()

        self.app_name_label = BodyLabel('app名称: ', self)
        self.app_package_label = BodyLabel('app包名: ', self)
        self.app_version_label = BodyLabel('app版本: ', self)
        self.download_url_label = BodyLabel('下载短链接: ', self)
        self.download_method_label = BodyLabel('下载方式: ', self)

        vbox1.addWidget(self.app_name_label)
        vbox1.addWidget(self.app_package_label)
        vbox1.addWidget(self.app_version_label)
        vbox1.addWidget(self.download_url_label)
        vbox1.addWidget(self.download_method_label)

        self.app_name_edit = LineEdit(self)
        self.app_package_edit = LineEdit(self)
        self.app_version_edit = LineEdit(self)
        self.download_url_edit = LineEdit(self)
        self.download_method_edit = LineEdit(self)

        self.app_name_edit.setText(obj_.app_name)
        self.app_package_edit.setText(obj_.package_name)
        self.app_version_edit.setText(obj_.version)
        self.download_url_edit.setText(obj_.download_link)
        self.download_method_edit.setText(obj_.download_method)

        self.app_name_edit.setReadOnly(True)
        self.app_package_edit.setReadOnly(True)
        self.app_version_edit.setReadOnly(True)
        self.download_url_edit.setReadOnly(True)
        self.download_method_edit.setReadOnly(True)

        vbox2.addWidget(self.app_name_edit)
        vbox2.addWidget(self.app_package_edit)
        vbox2.addWidget(self.app_version_edit)
        vbox2.addWidget(self.download_url_edit)
        vbox2.addWidget(self.download_method_edit)

        hbox1.addLayout(vbox1)
        hbox1.addLayout(vbox2)

        self.viewLayout.addLayout(hbox1)

        # change the text of button
        self.yesButton.setText('确定')
        self.yesButton.disconnect()
        self.yesButton.clicked.connect(self.validate)
        self.cancelButton.setText('关闭')

        self.widget.setMinimumWidth(500)

    def validate(self):
        self.accept()


class RadioButtonWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 添加布局
        layout = QVBoxLayout(self)

        self.comboBox = ComboBox(self)
        self.comboBox.setPlaceholderText("选择下载方式")

        items = ['store', 'apk']
        self.comboBox.addItems(items)
        self.comboBox.setCurrentIndex(-1)
        # self.comboBox.currentTextChanged.connect(print)

        # 将 ComboBox 添加到布局中
        layout.addWidget(self.comboBox)
        layout.setContentsMargins(0, 0, 0, 0)  # 设置边距为0

    def get_selected_method(self) -> str:
        """获取选择的下载方式"""
        return self.comboBox.currentText()
