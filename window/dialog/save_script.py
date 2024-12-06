from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QVBoxLayout, QDialog, QLabel, QPushButton, QHBoxLayout, QLineEdit, QTextEdit

from store_service.service.service_script import ScriptService
from store_service.model.model_script import Script


class SaveScriptDialog(QDialog):

    def __init__(self, script, parent):
        super().__init__()
        self.script = script
        self.__parent = parent

        self.setWindowTitle('脚本编辑')
        self.resize(500, 200)
        # 包名
        package_key = QLabel()
        package_key.setText("应用包名：")
        self.package_val = QLineEdit()
        self.package_val.setPlaceholderText("请输入应用包名")
        self.package_val.setText(script["package_name"])
        package_layout = QHBoxLayout()
        package_layout.addWidget(package_key, stretch=1)
        package_layout.addWidget(self.package_val, stretch=3)
        # 脚本名称
        name_key = QLabel()
        name_key.setText("脚本名称：")
        self.name_val = QLineEdit()
        self.name_val.setPlaceholderText("请输入脚本名称")
        self.name_val.setText(self.script["name"])
        name_layout = QHBoxLayout()
        name_layout.addWidget(name_key, stretch=1)
        name_layout.addWidget(self.name_val, stretch=3)
        # 名称和脚本名布局
        name_package_layout = QHBoxLayout()
        name_package_layout.addLayout(package_layout, stretch=1)
        name_package_layout.addLayout(name_layout, stretch=1)
        # 脚本内容
        content_key = QLabel()
        content_key.setText("脚本内容：")
        self.content_val = QTextEdit()
        self.content_val.setPlaceholderText("请输入脚本内容")
        self.content_val.setText(script["content"])
        content_layout = QHBoxLayout()
        content_layout.addWidget(content_key, stretch=1)
        content_layout.addWidget(self.content_val, stretch=6)

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
        self.layout.addLayout(name_package_layout, stretch=1)
        self.layout.addLayout(content_layout, stretch=1)
        self.layout.addLayout(button_layout)

    def save(self):
        script_ = Script(script_name=self.name_val.text(),
                         app=self.package_val.text(),
                         script_content=self.content_val.toPlainText())
        ScriptService().insert_script(script_)

        # ScriptStore().add({
        #     "name": self.name_val.text(),
        #     "package_name": self.package_val.text(),
        #     "content": self.content_val.toPlainText()
        # })
        self.__parent.set_table_data()
        self.accept()
