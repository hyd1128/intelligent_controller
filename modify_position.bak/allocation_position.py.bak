#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/9/4 9:41
# @Author : limber
# @desc : 传入设备

import time
import random
from image.image import ImageMatch
from adb.adb import run_command
from logger_zk.logger_types import logger_run


# def appoint_position(device, package_name, longitude, latitude):
def appoint_position(device, package_name):
    # 1、返回主界面 返回两次 kill模拟定位软件进程
    back_home(device)
    time.sleep(1)
    back_home(device)
    time.sleep(1)
    kill_specified_process(device, package_name)

    # 2、截图 从手机端拉取图片到电脑端； 识别软件在主屏幕的的位置坐标；点击对应图标
    printscreen_pull(device)

    # 模板图像匹配
    point = ImageMatch("./modify_position/templates/logo.png", f"./modify_position/screens/{device}_screen.png").match()
    if point is not None:
        click(device, point[0], point[1])
        time.sleep(3)

    else:
        count = 0
        while True:
            printscreen_pull(device)
            point = ImageMatch("./modify_position/templates/logo.png", f"./modify_position/screens/{device}_screen.png").match()
            if point is not None:
                click(device, point[0], point[1])
                time.sleep(3)

                # 在主屏幕上找到了该图标 跳出循环
                break

            count += 1
            if count == 5:
                logger_run.info("在step1上找不到对应图标，流程结束")
                return False

    # 5、经纬度坐标 模拟指定经纬度坐标对应的地点
    # switch_position(device, longitude, latitude)
    time.sleep(3)

    # 返回主界面 返回两次
    back_home(device)
    time.sleep(1)
    back_home(device)
    time.sleep(1)
    return True


def click(device, x, y):
    run_command(f"adb -s {device} shell input tap {x} {y}")


def screen_cap(device):
    run_command(f"adb -s {device} shell screencap /sdcard/screenshot.png")


# 拉取截屏图片
def screen_cap_pull(device):
    run_command(f"adb -s {device} pull /sdcard/screenshot.png ./modify_position/screens/{device}_screen.png")
    return f"./screens/{device}_screen.png"


# 删除截屏图片
def screen_cap_delete(device):
    run_command(f"adb -s {device} shell rm /sdcard/screenshot.png")


# 返回主页
def back_home(device):
    run_command(f"adb -s {device} shell input keyevent KEYCODE_HOME")


# 返回上一页
def back(device):
    run_command(f"adb -s {device} shell input keyevent KEYCODE_BACK")


def printscreen_pull(device):
    screen_cap(device)
    time.sleep(1)
    screen_cap_pull(device)
    time.sleep(2)


def kill_specified_process(device, package_name):
    run_command(f"adb -s {device} shell am force-stop {package_name}")


def switch_position(device, longitude, latitude):
    run_command(
        f'adb -s {device} shell am broadcast -a "LU_LOC_RECEIVER" --efa "loc_data" {longitude},{latitude}')


def generate_coordinate(coord_1, coord_2):
    # 采用GCJ02坐标系，实用于高德地图，微信地图
    # 由于该查询坐标接口支持小数点后六位查询，所以在生成新坐标前将每一个坐标扩大1000000，使用新坐标的时候再缩小1000000
    coord_1_ = [i * 1000000 for i in coord_1]
    coord_2_ = [i * 1000000 for i in coord_2]

    # 生成新的经度坐标
    if coord_1_[0] < coord_2_[0]:
        longitude1, longitude2 = coord_1_[0], coord_2_[0]
    else:
        longitude1, longitude2 = coord_2_[0], coord_1_[0]
    new_longitude = random.randint(longitude1, longitude2)

    # 生成新的纬度坐标
    if coord_1_[1] < coord_2_[1]:
        latitude1, latitude2 = coord_1_[1], coord_2_[1]
    else:
        latitude1, latitude2 = coord_2_[1], coord_1_[1]
    new_latitude = random.randint(latitude1, latitude2)

    new_coord = [new_longitude, new_latitude]
    new_coord = [i / 1000000 for i in new_coord]

    return new_coord


if __name__ == '__main__':
    pass



