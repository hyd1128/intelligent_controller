#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2025/1/9 21:09
# @Author : limber
# @desc :
from typing import Any

from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QLabel, QWidget, QHBoxLayout

from qfluentwidgets import SwitchButton

from window_pyqt.component.general_widget import Widget
from window_pyqt.component.message_widget import MessageWidget


class HomeView(Widget):
    run_advertising_switch_signal = pyqtSignal(bool)

    def __init__(self, text: str, parent: Any = None):
        super().__init__(text=text, parent=parent)
        self.init_ui()

    def init_ui(self):
        self.widget_ = QtWidgets.QWidget(self)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_.sizePolicy().hasHeightForWidth())

        self.widget_.setSizePolicy(sizePolicy)
        self.widget_.setObjectName("widget_")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_)
        self.label_one = QLabel(parent=self.widget_)
        self.label_one.setText("广告开关 ")
        self.label_one.setStyleSheet("font-size: 16px;")
        self.horizontalLayout.addWidget(self.label_one)
        self.switchButton = SwitchButton(parent=self.widget_)
        self.horizontalLayout.addWidget(self.switchButton)
        spacerItem_h = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Expanding,
                                             QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addSpacerItem(spacerItem_h)
        self.switchButton.checkedChanged.connect(self.onCheckedChanged)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum,
                                           QtWidgets.QSizePolicy.Policy.Expanding)

        self.vBoxLayout.setContentsMargins(50, 30, 50, 30)
        self.vBoxLayout.addWidget(self.widget_)
        self.vBoxLayout.addItem(spacerItem)

    def onCheckedChanged(self, isChecked):
        text = 'On' if isChecked else 'Off'
        self.switchButton.setText(text)
        if isChecked:
            MessageWidget.success_message(self, "正在执行广告任务", duration=5000)
            self.run_advertising_switch_signal.emit(True)
        else:
            MessageWidget.warning_message(self, "关闭广告任务", duration=5000)
            self.run_advertising_switch_signal.emit(False)

