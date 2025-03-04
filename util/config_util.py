#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/19 16:21
# @Author : limber
# @desc :
import os

# 坐标1
COORD_ONE = [-74.001505, 40.761130]
# 坐标2
COORD_TWO = [-73.976442, 40.734079]

# 存放json文件、图片文件的文件夹名称
RESOURCES = "resources"

# 线程池文件名称
POOL_FILE_NAME = "pool.json"
# 线程池对应的key name
THREAD_POOL_SIZE = "thread_pool_size"

# date 格式
DATE_FORMAT = "%Y-%m-%d"
# date time 格式
DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

###### 广告线程 开关 #####
SWITCH = False


# 广告任务截取屏幕图片储存到当前项目的位置, 相对于当前工作目录
ADVERTISING_SCREENSHOT = os.path.join(RESOURCES, "screenshot")

# 图片匹配结果文件夹
MATCH_RESULT_FOLDER = os.path.join(RESOURCES, "image_match_result")

# 定位软件包名
LOCATING_APP_PACKAGE_NAME = "com.ziqi.luloc"
# google 包名
CHROME_PACKAGE_NAME = "com.android.chrome"
# prism 包名
PRISM_PACKAGE_NAME = "com.dexai.prism"
# 定位软件重启间隔时长 单位: 时
LOCATING_APP_RELOAD_INTERVAL_TIME = 1

# 定位任务模板图片文件夹 (相对工作目录位置)
LOCATING_TEMPLATE_FOLDER = os.path.join(RESOURCES, "locating_template")

# 广告模板文件夹
ADVERTISING_TEMPLATE = os.path.join(RESOURCES, "advertising_template", "advertising_icon_template")

# 当前节点信息文件路径, 相对于当前工作路径
NODE_DATA = os.path.join(RESOURCES, "node", "data.json")

# 当前登录节点的用户详细信息
CURRENT_USER_DETAIL = os.path.join(RESOURCES, "node", "current_user.json")

# AppTask task_type
# 下载app任务
APP_TASK_TYPE_ONE = "download"
# 更新app任务
APP_TASK_TYPE_TWO = "update"

# app市场模板路径
GOOGLE_PLAY_MARKET = os.path.join(RESOURCES, "google_play_market")
HUAWEI_MARKET = os.path.join(RESOURCES, "huawei_market")

# 下载app按钮模板路径
DOWNLOAD_APP_ICON = os.path.join(GOOGLE_PLAY_MARKET, "download.png")
# 更新app按钮模板路径
UPDATE_APP_ICON = os.path.join(GOOGLE_PLAY_MARKET, "update.png")
