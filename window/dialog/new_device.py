from PyQt6.QtWidgets import QVBoxLayout, QDialog, QLabel, QPushButton, QHBoxLayout
from PyQt6 import QtWidgets
from util.device_queue import DeviceQueue
from store_service.service.service_device import DeviceService
from store_service.model.model_device import Device


class NewDeviceDialog(QDialog):

    def __init__(self, device, parent):
        super().__init__()
        self.device = device
        self.__parent = parent

        self.setWindowTitle('新设备信息')
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
        version_val.setText(device["android_version"])
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
        resolution_val.setText(f"{device['resolution_ratio']}")
        resolution_layout = QHBoxLayout()
        resolution_layout.addWidget(resolution_key, stretch=1)
        resolution_layout.addWidget(resolution_val, stretch=8)

        # 按钮组
        add_btn = QtWidgets.QPushButton()
        add_btn.setText("添加设备")
        add_btn.setStyleSheet("background:rgb(0, 85, 255);color:white;")
        add_btn.clicked.connect(self.add)
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(add_btn)

        # 整体布局
        layout = QVBoxLayout(self)
        layout.addLayout(device_id_brand_layout, stretch=1)
        layout.addLayout(manufacturer_version_layout, stretch=1)
        layout.addLayout(resolution_layout, stretch=1)
        layout.addLayout(btn_layout, stretch=1)

    def add(self):
        self.device["online_state"] = 1
        self.device["task_state"] = 0
        self.device["locating_app_status"] = 0

        # 查询该设备的device_id是否存在, 不存在则为新设备
        result = DeviceService().select_by_device_id(self.device["device_id"])

        # 判断是否为新设备
        if result is None:
            # 实例化一个Device对象
            device_ = Device(**self.device)
            DeviceService().add_device(device_)
            # 将新设备添加到队列
            new_device = DeviceService().select_by_device_id(device_.device_id)
            DeviceQueue.put(new_device)
            # DeviceQueue.put(device_)
            # 刷新页面
            self.__parent.set_device_page_data()
            self.accept()
