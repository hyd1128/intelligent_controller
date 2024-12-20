#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/11/5 9:15
# @Author : limber
# @desc :
import time
from random import random

from adb.adb import back_home, screen_cap, screen_cap_pull, back, swipe, stop_app, click
from global_var import package_prism, package_innova, package_calculator
from image.image import ImageMatch


def run_run_app(script: str, device_id: str) -> None:
    """
    根据脚本和设备编号初始化app
    
    :param script: 
    :param device_id: 
    :return: 
    """

    """
        设备执行
    
        当前程序写的一些脚本命令:
            - home：返回主界面
            - waiting: 等待广告时间
            - adv: 广告退出坐标匹配
            - swipe: 滑动
            - back: 返回上一级
            - kill: 杀死对应程序进程
    """

    # 返回主界面
    if script == "home":
        back_home(device_id)
        time.sleep(3)

    # 广告时间等待功能
    elif script == "waiting":
        # 范围随机广告等待时间
        adv_time = random.randint(45, 70)
        time.sleep(adv_time)

    # 匹配广告图标并退出广告界面
    elif script == "adv":
        back(device_id)

        time.sleep(3)

    # 滑动页面
    elif script == "swipe":
        start_coord = [540, 1600]
        end_coord = [540, 800]
        duration_time = 100  # ms
        swipe(device_id, start_coord, end_coord, duration_time)

    # back 返回上一级或者退出广告界面
    elif script == "back":
        back(device_id)

    # kill进程
    elif script == "kill":
        if script.app == "prism":
            stop_app(device_id, package_prism)

        elif script.app == "innova":
            stop_app(device_id, package_innova)

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
            # 此时这种情况已经无法匹配对应点，后续步骤已经无法按计划进行，所以这个脚本暂停执行
            #   1、返回桌面
            #   2、更新手机状态，并将手机放回到全局队列中
            #   3、关闭模拟定位后台进程
            #   4、关闭被操作软件包进程
            back_home(device_id)
        # 已匹配到则点击
        click(device_id, point[0], point[1])
        time.sleep(5)

