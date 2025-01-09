#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2025/1/6 17:06
# @Author : limber
# @desc :
from typing import Any

from PyQt6.QtCore import Qt
from qfluentwidgets import InfoBar, InfoBarIcon, InfoBarPosition


class MessageWidget:
    @staticmethod
    def info_message(parent: Any, content: str):
        """
        :param parent: 父组件
        :param content: 子组件
        :return:
        """
        w = InfoBar(
            icon=InfoBarIcon.INFORMATION,
            title='info',
            content=content,
            orient=Qt.Orientation.Horizontal,  # vertical layout
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=parent
        )
        w.show()

    @staticmethod
    def success_message(parent: Any, content: str, duration=2000):
        # convenient class mothod
        InfoBar.success(
            title='success',
            content=content,
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            # position='Custom',   # NOTE: use custom info bar manager
            duration=duration,
            parent=parent
        )

    @staticmethod
    def warning_message(parent: Any, content: str, duration=2000):
        InfoBar.warning(
            title='warning',
            content=content,
            orient=Qt.Orientation.Horizontal,
            isClosable=True,  # disable close button
            position=InfoBarPosition.TOP_RIGHT,
            duration=duration,
            parent=parent
        )

    @staticmethod
    def error_message(parent: Any, content: str):
        InfoBar.error(
            title="error",
            content=content,
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,  # won't disappear automatically
            parent=parent
        )
