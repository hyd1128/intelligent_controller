#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2025/1/3 15:27
# @Author : limber
# @desc :
import math
from typing import Any

from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QTableWidgetItem, QVBoxLayout, QWidget
from qfluentwidgets import TableWidget, PrimaryPushButton, MessageBoxBase, BodyLabel, LineEdit, ComboBox, TextEdit, \
    PlainTextEdit

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
        self.paging_widget.update_page_signal.connect(self.update_page)

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
        self.tableView.setColumnCount(5)
        self.vBoxLayout.setContentsMargins(50, 30, 50, 30)

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
        songInfos = [
            ['かばん', 'aiko', 'かばん', '2004', '5:04'],
            ['爱你', '王心凌', '爱你', '2004', '3:39'],
            ['星のない世界', 'aiko', '星のない世界/横顔', '2007', '5:30'],
            ['横顔', 'aiko', '星のない世界/横顔', '2007', '5:06'],
            ['秘密', 'aiko', '秘密', '2008', '6:27'],
            ['シアワセ', 'aiko', '秘密', '2008', '5:25'],
            ['二人', 'aiko', '二人', '2008', '5:00'],
            ['スパークル', 'RADWIMPS', '君の名は。', '2016', '8:54'],
            ['なんでもないや', 'RADWIMPS', '君の名は。', '2016', '3:16'],
            ['前前前世', 'RADWIMPS', '人間開花', '2016', '4:35'],
            ['恋をしたのは', 'aiko', '恋をしたのは', '2016', '6:02'],
            ['夏バテ', 'aiko', '恋をしたのは', '2016', '4:41'],
            ['もっと', 'aiko', 'もっと', '2016', '4:50'],
            ['問題集', 'aiko', 'もっと', '2016', '4:18'],
            ['半袖', 'aiko', 'もっと', '2016', '5:50'],
            ['ひねくれ', '鎖那', 'Hush a by little girl', '2017', '3:54'],
            ['シュテルン', '鎖那', 'Hush a by little girl', '2017', '3:16'],
            ['愛は勝手', 'aiko', '湿った夏の始まり', '2018', '5:31'],
            ['ドライブモード', 'aiko', '湿った夏の始まり', '2018', '3:37'],
            ['うん。', 'aiko', '湿った夏の始まり', '2018', '5:48'],
            ['キラキラ', 'aikoの詩。', '2019', '5:08', 'aiko'],
            ['恋のスーパーボール', 'aiko', 'aikoの詩。', '2019', '4:31'],
            ['磁石', 'aiko', 'どうしたって伝えられないから', '2021', '4:24'],
            ['食べた愛', 'aiko', '食べた愛/あたしたち', '2021', '5:17'],
            ['列車', 'aiko', '食べた愛/あたしたち', '2021', '4:18'],
            ['花の塔', 'さユり', '花の塔', '2022', '4:35'],
            ['夏恋のライフ', 'aiko', '夏恋のライフ', '2022', '5:03'],
            ['あかときリロード', 'aiko', 'あかときリロード', '2023', '4:04'],
            ['荒れた唇は恋を失くす', 'aiko', '今の二人をお互いが見てる', '2023', '4:07'],
            ['ワンツースリー', 'aiko', '今の二人をお互いが見てる', '2023', '4:47'],
        ]
        self.paging_widget.update_page_amount(math.ceil(len(songInfos) / 15))
        start_ = 15 * (page_number - 1)
        end_ = start_ + 15
        songInfos = songInfos[start_:end_]
        for i, songInfo in enumerate(songInfos):
            for j in range(5):
                self.tableView.setItem(i, j, QTableWidgetItem(songInfo[j]))

        self.tableView.verticalHeader().hide()
        self.tableView.resizeColumnsToContents()
        self.tableView.setHorizontalHeaderLabels(['Title', 'Artist', 'Album', 'Year', 'Duration'])
        # self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        # self.tableView.setSortingEnabled(True)

        self.setStyleSheet("Demo{background: rgb(255, 255, 255)} ")

    def update_page(self, page_number):
        self.init_table_data(page_number)

    def show_add_script_dialog(self):
        w = AddScriptDialog(self)
        if w.exec():
            MessageWidget.success_message(self, content="添加成功")
        else:
            MessageWidget.error_message(self, content="添加失败")


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

        vbox1.addWidget(self.script_name_label)
        vbox1.addWidget(self.script_content_label)
        vbox1.addWidget(self.script_type_label)

        self.script_name_edit = LineEdit(self)
        self.script_content_edit = PlainTextEdit(self)
        self.script_content_edit.setFixedSize(500, 120)
        self.script_type_edit = RadioButtonWidget()

        vbox2.addWidget(self.script_name_edit)
        vbox2.addWidget(self.script_content_edit)
        vbox2.addWidget(self.script_type_edit)

        hbox1.addLayout(vbox1)
        hbox1.addLayout(vbox2)

        self.script_name_edit.setClearButtonEnabled(True)
        # self.script_content_edit.setClearButtonEnabled(True)

        self.viewLayout.addLayout(hbox1)

        # change the text of button
        self.yesButton.setText('添加app')
        self.cancelButton.setText('取消')

        self.widget.setMinimumWidth(500)


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
