#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/11/10 23:04
# @Author : limber
# @desc :

# package name
prism_package_name = "com.dexai.prism"
chrome_package_name = "com.android.chrome"
google_store_package_name = "com.android.vending"
x_package_name = "com.twitter.android"
youtube_package_name = "com.google.android.youtube"

# input content
prism_app_name = "prism"
x_app_name = "x"
chrome_app_name = "chrome"
youtube_app_name = "youtube"

# download script 基于主文件路径
download_script = [
    "kill",
    "home",
    "home",
    "q_threads/scripts/download_script_template/store_icon.png",
    "q_threads/scripts/download_script_template/search_module.png",
    "q_threads/scripts/download_script_template/search_box.png",
    "input",
    "q_threads/scripts/download_script_template/search_button.png",
    "q_threads/scripts/update_script_template/youtube_icon.png",
    "q_threads/scripts/download_script_template/install_icon.png",
    "home"
    "kill"
]

# update script 基于主文件路径
update_script = [
    "kill",
    "home",
    "home",
    "q_threads/scripts/download_script_template/store_icon.png",
    "q_threads/scripts/download_script_template/search_module.png",
    "q_threads/scripts/download_script_template/search_box.png",
    "input",
    "q_threads/scripts/download_script_template/search_button.png",
    "q_threads/scripts/update_script_template/youtube_icon.png",
    "q_threads/scripts/update_script_template/upload_icon.png",
    "home",
    "kill"
]

# 授权app脚本
authorization_script = []
