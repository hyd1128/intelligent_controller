from PyQt6.QtWidgets import QVBoxLayout, QDialog, QLabel, QPushButton, QHBoxLayout
from PyQt6 import QtWidgets


class OfflineDeviceDialog(QDialog):

    def __init__(self, device):
        super().__init__()
        self.device = device

        if device["online"] == "online":
            self.setWindowTitle('设备上线通知')
        else:
            self.setWindowTitle('设备离线通知')

        self.resize(500, 200)
        # 设备号
        device_id_key = QLabel()
        device_id_key.setText("设备号：")
        device_id_val = QLabel()
        device_id_val.setText(device["device_id"])
        device_id_layout = QHBoxLayout()
        device_id_layout.addWidget(device_id_key, stretch=1)
        device_id_layout.addWidget(device_id_val, stretch=3)
        # 品牌
        brand_key = QLabel()
        brand_key.setText('品牌：')
        brand_val = QLabel()
        brand_val.setText(device["brand"])
        brand_layout = QHBoxLayout()
        brand_layout.addWidget(brand_key, stretch=1)
        brand_layout.addWidget(brand_val, stretch=3)
        # 设备号和品牌布局
        device_id_brand_layout = QHBoxLayout()
        device_id_brand_layout.addLayout(device_id_layout, stretch=1)
        device_id_brand_layout.addLayout(brand_layout, stretch=1)

        # 厂商
        manufacturer_key = QLabel()
        manufacturer_key.setText("厂  商：")
        manufacturer_val = QLabel()
        manufacturer_val.setText(device["manufacturer"])
        manufacturer_layout = QHBoxLayout()
        manufacturer_layout.addWidget(manufacturer_key, stretch=1)
        manufacturer_layout.addWidget(manufacturer_val, stretch=3)
        # Android版本号
        version_key = QLabel()
        version_key.setText('Android版本号：')
        version_val = QLabel()
        version_val.setText(device["version"])
        version_layout = QHBoxLayout()
        version_layout.addWidget(version_key, stretch=1)
        version_layout.addWidget(version_val, stretch=3)
        # 设备号和品牌布局
        manufacturer_version_layout = QHBoxLayout()
        manufacturer_version_layout.addLayout(manufacturer_layout, stretch=1)
        manufacturer_version_layout.addLayout(version_layout, stretch=1)

        # 分辨率
        resolution_key = QLabel()
        resolution_key.setText('分辨率：')
        resolution_val = QLabel()
        resolution_val.setText(f"{device['resolution'][0]} x {device['resolution'][1]}")
        resolution_layout = QHBoxLayout()
        resolution_layout.addWidget(resolution_key, stretch=1)
        resolution_layout.addWidget(resolution_val, stretch=8)

        # 按钮组
        close_btn = QtWidgets.QPushButton()
        close_btn.setText("关闭")
        close_btn.setStyleSheet("background:rgb(0, 85, 255);color:white;")
        close_btn.clicked.connect(self.close)
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(close_btn)

        # 整体布局
        layout = QVBoxLayout(self)
        layout.addLayout(device_id_brand_layout, stretch=1)
        layout.addLayout(manufacturer_version_layout, stretch=1)
        layout.addLayout(resolution_layout, stretch=1)
        layout.addLayout(btn_layout, stretch=1)

    def close(self):
        self.accept()
