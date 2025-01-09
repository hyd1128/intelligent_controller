#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2025/1/3 18:44
# @Author : limber
# @desc :

import sys
from PyQt6 import QtWidgets
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QApplication, QWidget
from qfluentwidgets import BodyLabel, LineEdit, ToolButton, FluentIcon, InfoBar, InfoBarPosition, InfoBarIcon

from window_pyqt.component.message_widget import MessageWidget


class PagingWidget(QWidget):
    update_page_signal = pyqtSignal(int)

    def __init__(self, parent=None):
        """

        :param page: 总页数
        """
        super().__init__()
        self.page_number_ = 1
        self.page_amount = 1
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        self.setObjectName("paging_widget")

        # 为 PagingWidget 创建主布局
        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.widget = QtWidgets.QWidget(parent=self)
        self.widget.setFixedSize(374, 35)
        self.widget.setObjectName("widget")

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.widget.setLayout(self.horizontalLayout)

        # 将两个 spacerItem 都设置为 Expanding
        spacerItem1 = QtWidgets.QSpacerItem(174, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                            QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)

        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.left_button = ToolButton(FluentIcon.CARE_LEFT_SOLID)
        self.left_button.clicked.connect(self.update_page_nbumber)
        self.right_button = ToolButton(FluentIcon.CARE_RIGHT_SOLID)
        self.right_button.clicked.connect(self.update_page_nbumber)
        self.horizontalLayout.addWidget(self.left_button)
        self.horizontalLayout.addWidget(self.right_button)

        self.label = BodyLabel("当前第")
        self.label.setTextColor(QColor(0, 0, 0))
        self.horizontalLayout.addWidget(self.label)

        self.page_ = LineEdit()
        self.page_.setText(str(self.page_number_))
        self.page_.setReadOnly(True)
        self.horizontalLayout.addWidget(self.page_)

        self.label_2 = BodyLabel("页, 共")
        self.label_2.setTextColor(QColor(0, 0, 0))
        self.horizontalLayout.addWidget(self.label_2)

        self.total_page_ = LineEdit()
        self.total_page_.setText(str(self.page_amount))
        self.total_page_.setReadOnly(True)
        self.horizontalLayout.addWidget(self.total_page_)

        self.label_3 = BodyLabel("页")
        self.label_3.setTextColor(QColor(0, 0, 0))
        self.horizontalLayout.addWidget(self.label_3)

        spacerItem2 = QtWidgets.QSpacerItem(174, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                            QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)

        # 将 widget 添加到主布局中
        main_layout.addWidget(self.widget)

    def update_page_amount(self, page_amount: int):
        self.page_amount = page_amount
        self.total_page_.setText(str(page_amount))

    def update_page_nbumber(self):
        sender = self.sender()
        if sender == self.left_button:
            if self.page_number_ > 1:
                self.page_number_ -= 1
                self.change_page_number()
                self.update_page_signal.emit(self.page_number_)
            else:
                MessageWidget.warning_message(parent=self.parent, content="当前已是第一页")

        elif sender == self.right_button:
            if self.page_number_ < self.page_amount:
                self.page_number_ += 1
                self.change_page_number()
                self.update_page_signal.emit(self.page_number_)
            else:
                MessageWidget.warning_message(parent=self.parent, content="当前已是最后一页")

    def change_page_number(self):
        self.page_.setText(str(self.page_number_))

    def general_info(self, content: str):
        w = InfoBar(
            icon=InfoBarIcon.INFORMATION,
            title='提示',
            content=content,
            orient=Qt.Orientation.Horizontal,  # vertical layout
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=self.parent
        )
        w.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = PagingWidget()
    ui.show()
    sys.exit(app.exec())



