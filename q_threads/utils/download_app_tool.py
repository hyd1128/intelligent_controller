#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/11/4 23:00
# @Author : limber
# @desc :
import time

from adb.adb import back_home, back, screen_cap, screen_cap_pull, click, input_text, stop_app
from image.image import ImageMatch
from q_threads.module_varchar import google_store_package_name


def run_download_app(script: str, device_id: str):
    """
    根据传递过来的设备id和脚本内容执行相应的步骤

    设备执行
     当前程序写的一些脚本命令:
         - home：返回主界面
         - swipe: 滑动
         - back: 返回上一级
         - kill: kill应用进程

    :param script:
    :param device_id:
    :return:
    """
    # 返回主界面
    if script == "home":
        back_home(device_id)
        time.sleep(3)

    # back 返回上一级
    elif script == "back":
        back(device_id)
        time.sleep(3)

    # 根据匹配的坐标进行输入
    elif script == "input":
        input_text(device_id, "youtube")
        time.sleep(3)

    elif script == "kill":
        stop_app(device_id, google_store_package_name)
        time.sleep(3)

    else:
        # 当前状况为模板匹配并根据图标进行点击
        # 重试时长
        retry_duration = 0

        # 截屏
        screen_cap(device_id)
        time.sleep(2)

        # 拉取屏幕图片
        screen_image = screen_cap_pull(device_id)
        time.sleep(5)

        # 匹配
        point = ImageMatch(script, screen_image).match()

        # 未匹配到则重复匹配-每次等待10秒钟且总等待时间不超过40秒钟
        while point is None and retry_duration <= 30:
            retry_duration += 10

            # 截屏
            screen_cap(device_id)
            time.sleep(1)

            # 拉取屏幕图片
            screen_image = screen_cap_pull(device_id)
            time.sleep(2)
            point = ImageMatch(script, screen_image).match()

        # 未匹配到则不再执行且返回首页
        if point is None:
            back_home(device_id)
            stop_app(device_id, google_store_package_name)
            return

        # 已匹配到则点击
        click(device_id, point[0], point[1])
        time.sleep(5)
