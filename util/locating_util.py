#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/20 12:00
# @Author : limber
# @desc :
import time

from logger_zk.logger_types import logger_run
from util.adb_util import AdbUtil
from util.config_util import LOCATING_TEMPLATE_FOLDER
from util.image_util import ImageUtil
from util.path_util import PathUtil
from util.uiautomotor_util import UIAutoMotorUtil


class LocatingUtil:
    @staticmethod
    def enable_positioning(device_id: str, package_name: str) -> bool:
        """
        根据设备id和包名开启定位软件

        :param device_id:
        :param package_name:
        :return:
        """
        # # 1. 返回主界面 返回两次 kill模拟定位软件进程
        # AdbUtil.back_home(device_id)
        # time.sleep(1)
        # AdbUtil.back_home(device_id)
        # time.sleep(1)
        # AdbUtil.stop_app(device_id, package_name)
        #
        # # 2. 截图, 从手机端拉取图片到电脑端, 识别软件在主屏幕的的位置坐标, 点击对应图标
        # AdbUtil.screen_cap(device_id)
        # time.sleep(1)
        # target_path = AdbUtil.screen_cap_pull(device_id)
        # time.sleep(1)
        #
        # # 3. 模板匹配
        # root_path = PathUtil.get_root_path(__file__, 2)
        # template_path = str(root_path.joinpath(LOCATING_TEMPLATE_FOLDER).joinpath("logo.png"))
        # point = ImageUtil.match(target_path=target_path,
        #                         template_path=template_path)
        # if point is not None:
        #     AdbUtil.click(device_id, point[0], point[1])
        #     time.sleep(3)
        # else:
        #     count = 0
        #     while True:
        #         AdbUtil.screen_cap(device_id)
        #         time.sleep(1)
        #         target_path = AdbUtil.screen_cap_pull(device_id)
        #         time.sleep(1)
        #         point = ImageUtil.match(target_path=target_path,
        #                                 template_path=template_path)
        #         if point is not None:
        #             AdbUtil.click(device_id, point[0], point[1])
        #             time.sleep(3)
        #             # 跳出循环
        #             break
        #         count += 1
        #         if count == 5:
        #             logger_run.info("##### 在step1上找不到对应图标, 流程结束 #####")
        #             return False
        # time.sleep(3)
        # # 返回设备主屏幕界面
        # AdbUtil.back_home(device_id)
        # time.sleep(1)
        # AdbUtil.back_home(device_id)
        # time.sleep(1)
        # return True

        ######################
        # 新的群控定位软件开启方式
        ######################

        try:
            UIAutoMotorUtil.home(device_id)
            UIAutoMotorUtil.home(device_id)
            time.sleep(2)
            UIAutoMotorUtil.stop_app(package_name)
            time.sleep(2)
            UIAutoMotorUtil.start_app(package_name)
            return True
        except Exception as e:
            logger_run.error(f"启动定位软件过程中出现异常, 异常详情: {str(e)}")
            return False



