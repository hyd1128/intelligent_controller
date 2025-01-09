#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2025/1/3 15:13
# @Author : limber
# @desc :
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QLabel, QHBoxLayout, QVBoxLayout


class Widget(QFrame):

    def __init__(self, text: str, parent: object = None) -> object:
        super().__init__(parent=parent)
        self.setObjectName(text.replace(' ', '-'))
        self.label = QLabel(text, self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.addWidget(self.label)

        # leave some space for title bar
        self.vBoxLayout.setContentsMargins(0, 32, 0, 0)
