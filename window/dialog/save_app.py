from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QVBoxLayout, QDialog, QLabel, QPushButton, QHBoxLayout, QLineEdit, QFileDialog
from store_service.service.service_app import AppService
from store_service.model.model_app import App


class SaveAppDialog(QDialog):

    def __init__(self, app, parent):
        super().__init__()
        self.app = app
        self.__parent = parent

        self.setWindowTitle('应用编辑')
        self.resize(500, 200)

        # label
        name_key = QLabel()
        name_key.setText("应用名")
        package_key = QLabel()
        package_key.setText("包名")
        # label布局
        label_layout = QVBoxLayout()
        label_layout.addWidget(name_key)
        label_layout.addWidget(package_key)

        # edit
        self.name_val = QLineEdit()
        self.name_val.setPlaceholderText("请输入应用名")
        self.name_val.setText(self.app["name"])
        self.package_val = QLineEdit()
        self.package_val.setPlaceholderText("请输入包名")
        self.package_val.setText(app["package_name"])
        # edit布局
        edit_layout = QVBoxLayout()
        edit_layout.addWidget(self.name_val)
        edit_layout.addWidget(self.package_val)

        # label edit水平布局
        label_edit_layout = QHBoxLayout()
        label_edit_layout.addLayout(label_layout)
        label_edit_layout.addLayout(edit_layout, stretch=3)

        # button
        button_layout = QHBoxLayout()
        spacer_left = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Policy.Expanding,
                                            QtWidgets.QSizePolicy.Policy.Minimum)
        spacer_right = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Policy.Expanding,
                                             QtWidgets.QSizePolicy.Policy.Minimum)
        save_btn = QPushButton()
        save_btn.setText("保存")
        save_btn.clicked.connect(self.save)
        button_layout.addItem(spacer_left)
        button_layout.addWidget(save_btn)
        button_layout.addItem(spacer_right)

        # 总体布局
        self.layout = QVBoxLayout(self)
        self.layout.addLayout(label_edit_layout)
        self.layout.addLayout(button_layout)

    def save(self):
        app_ = App(app_name=self.name_val.text())
        AppService().add_app(app_)
        # AppStore().add({
        #     "name": self.name_val.text(),
        #     "package_name": self.package_val.text()
        # })
        self.__parent.set_table_data()
        self.accept()
