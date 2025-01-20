#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2025/1/17 9:15
# @Author : limber
# @desc :
import dis
from typing import List, Tuple

import uiautomator2 as uam2


class UIAutoMotorUtil:

    @staticmethod
    def home(device_id: str) -> bool:
        try:
            device_ = uam2.connect(serial=device_id)
            device_.press("home")
            return True
        except Exception as e:
            print(e)
            raise e

    @staticmethod
    def back(device_id: str) -> bool:
        try:
            device_ = uam2.connect(serial=device_id)
            device_.press("back")
            return True
        except Exception as e:
            print(e)
            raise e

    @staticmethod
    def click_by_xpath(device_id: str, element_xpath: str) -> bool:
        try:
            device_ = uam2.connect(serial=device_id)
            device_.xpath(element_xpath).click()
            return True
        except Exception as e:
            print(e)
            raise e


    @staticmethod
    def click_by_coord(device_id: str, coord_: List[int]) -> bool:
        try:
            device_ = uam2.connect(serial=device_id)
            device_.click(x=coord_[0], y=coord_[1])
            return True
        except Exception as e:
            print(e)
            raise e

    @staticmethod
    def swipe_by_coord(device_id: str, coord_: List[Tuple[int, int]], duration: float = 0.5) -> bool:
        try:
            device_ = uam2.connect(serial=device_id)
            device_.swipe_points(coord_, duration=duration)
            return True
        except Exception as e:
            print(e)
            raise e

    @staticmethod
    def start_app(device_id: str, app_package_name: str) -> bool:
        try:
            device_ = uam2.connect(serial=device_id)
            device_.app_start(package_name=app_package_name)
            return True
        except Exception as e:
            print(e)
            raise e

    @staticmethod
    def stop_app(device_id: str, app_package_name: str) -> bool:
        try:
            device_ = uam2.connect(serial=device_id)
            device_.app_stop(package_name=app_package_name)
            return True
        except Exception as e:
            print(e)
            raise e

    @staticmethod
    def delete_app(device_id: str, app_package_name: str) -> bool:
        try:
            device_ = uam2.connect(serial=device_id)
            device_.app_uninstall(package_name=app_package_name)
            return True
        except Exception as e:
            print(e)
            raise e

    @staticmethod
    def input_text(device_id: str, text_content: str) -> bool:
        try:
            device_ = uam2.connect(serial=device_id)
            device_.send_keys(text_content)
            return True
        except Exception as e:
            print(e)
            raise e

    @staticmethod
    def enter(device_id: str):
        try:
            device_ = uam2.connect(serial=device_id)
            device_.send_action()
            return True
        except Exception as e:
            print(e)
            raise e

    @staticmethod
    def app_list(device_id: str) -> List:
        try:
            device_id = uam2.connect(serial=device_id)
            app_list = device_id.app_list()
            return app_list
        except Exception as e:
            print(e)
            raise e

    @staticmethod
    def is_download_app(device_id: str, app_package_name: str) -> bool:
        try:
            device_ = uam2.connect(serial=device_id)
            app_list = device_.app_list()
            if app_package_name in app_list:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            raise e

    def generate_uam(self, device_id: str) -> uam2.Device:
        return uam2.connect(serial=device_id)
