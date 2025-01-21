#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2025/1/22 0:55
# @Author : limber
# @desc :
import time

import uiautomator2 as uam2

from database_service.model.device_model import Device
from util.device_queue import DeviceQueue


class ManageAppUtil:

    @staticmethod
    def download_app(device: Device, app_short_link: str) -> bool:
        try:
            d = uam2.connect(serial=device.device_id)
            time.sleep(1)
            d.press("home")
            time.sleep(1)
            d.press("home")
            # 1. 启动google chrome
            d.app_start("com.android.chrome")
            time.sleep(2)

            # 2. 点击进入chrome 主界面
            widget_ = d.xpath('//*[@resource-id="com.android.chrome:id/home_button"]').exists
            if widget_:
                d.xpath('//*[@resource-id="com.android.chrome:id/home_button"]').click()
                time.sleep(2)
            else:
                raise Exception("未找到该组件")

            # 3. 点击输入框
            widget_ = d.xpath('//*[@resource-id="com.android.chrome:id/url_bar"]').exists
            if widget_:
                d.xpath('//*[@resource-id="com.android.chrome:id/url_bar"]').click()
                time.sleep(2)
            else:
                raise Exception("未找到该组件")

            # 4. 输入框输入短链接
            d.send_keys(app_short_link)
            time.sleep(1)

            # 5. 确认搜索
            d.send_action()
            time.sleep(3)

            # 6. 进入google play界面
            widget_ = d.xpath('//*[@resource-id="com.android.chrome:id/message_primary_button"]').exists
            if widget_:
                d.xpath('//*[@resource-id="com.android.chrome:id/message_primary_button"]').click()
                time.sleep(3)
            else:
                raise Exception("未找到该组件")

            # 7. 点击下载按钮
            widget_ = d.xpath('//android.widget.TextView[@text="Install"]').exists
            if widget_:
                d.xpath('//android.widget.TextView[@text="Install"]').click()
                time.sleep(3)
            else:
                raise Exception("未找到该组件")

            # 8. 返回桌面
            d.press("home")
            return True
        except Exception as e:
            print(str(e))
            return False
        finally:
            DeviceQueue.put(device)

    @staticmethod
    def update_app(device: Device, app_short_link: str) -> bool:
        try:
            d = uam2.connect(serial=device.device_id)
            time.sleep(1)
            d.press("home")
            time.sleep(1)
            d.press("home")
            # 1. 启动google chrome
            d.app_start("com.android.chrome")
            time.sleep(2)

            # 2. 点击进入chrome 主界面
            widget_ = d.xpath('//*[@resource-id="com.android.chrome:id/home_button"]').exists
            if widget_:
                d.xpath('//*[@resource-id="com.android.chrome:id/home_button"]').click()
                time.sleep(2)
            else:
                raise Exception("未找到该组件")

            # 3. 点击输入框
            widget_ = d.xpath('//*[@resource-id="com.android.chrome:id/url_bar"]').exists
            if widget_:
                d.xpath('//*[@resource-id="com.android.chrome:id/url_bar"]').click()
                time.sleep(2)
            else:
                raise Exception("未找到该组件")

            # 4. 输入框输入短链接
            d.send_keys(app_short_link)
            time.sleep(1)

            # 5. 确认搜索
            d.send_action()
            time.sleep(3)

            # 6. 进入google play界面
            widget_ = d.xpath('//*[@resource-id="com.android.chrome:id/message_primary_button"]').exists
            if widget_:
                d.xpath('//*[@resource-id="com.android.chrome:id/message_primary_button"]').click()
                time.sleep(3)
            else:
                raise Exception("未找到该组件")

            # 7. 点击更新按钮
            widget_ = d.xpath('//android.widget.TextView[@text="Update"]').exists
            if widget_:
                d.xpath('//android.widget.TextView[@text="Update"]').click()
                time.sleep(3)
            else:
                raise Exception("未找到该组件")

            # 8. 返回桌面
            d.press("home")
            return True
        except Exception as e:
            print(str(e))
            return False
        finally:
            DeviceQueue.put(device)

    @staticmethod
    def delete_app(device: Device, app_package_name: str) -> bool:
        try:
            d = uam2.connect(serial=device.device_id)
            time.sleep(1)
            d.app_uninstall(app_package_name)
            time.sleep(2)
            d.press("home")
            time.sleep(2)
            return True
        except Exception as e:
            print(str(e))
            return False
        finally:
            DeviceQueue.put(device)
