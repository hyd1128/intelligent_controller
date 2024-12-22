#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/20 11:13
# @Author : limber
# @desc :
import subprocess
from pathlib import Path

from util.config_util import ADVERTISING_SCREENSHOT
from util.path_util import PathUtil


class AdbUtil:
    @staticmethod
    def run_shell_command(command: str) -> tuple:
        try:
            result = subprocess.run(command,
                                    shell=True,
                                    check=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,  # 如果将stderr设置未subprocess.STDOUT的话，输出和错误输出会合并到一起
                                    text=True,
                                    encoding='utf-8'
                                    )
            # cmd打印处出来的内容也会被stderr获取到
            if result.stderr and result.returncode != 0:
                return None, result.stderr
            return result.stdout, None
        except subprocess.CalledProcessError as e:
            return None, e.stderr

    @staticmethod
    def device_list() -> tuple:
        """
            获取设备列表

            示例: ['192.168.31.182:37651']
            """
        devices, err = AdbUtil.run_shell_command("adb devices")
        if err:
            return None, err
        lines = devices.strip().split('\n')
        device_lines = lines[1:]
        devices = [line.split()[0] for line in device_lines if line.strip()]
        return devices, None

    @staticmethod
    def info(device: str) -> tuple:
        """获取手机的品牌、 android版本号、厂商、分辨率"""

        # 品牌、Android版本号、厂商
        try:
            result, err = AdbUtil.run_shell_command(f"adb -s {device} shell getprop")
            if err:
                return None, err
            properties = {}
            lines = result.strip().split('\n')
            for line in lines:
                if ": " in line:
                    key, value = line.split(": ", 1)
                    key = key.strip().strip("[]")
                    value = value.strip().strip("[]")
                    properties[key] = value

            # 分辨率
            result, err = AdbUtil.run_shell_command(f"adb -s {device} shell wm size")
            if err:
                return None, err
            for line in result.strip().split('\n'):
                if "Physical size" in line:
                    resolution = line.split(": ")[1].strip()
                    properties["resolution"] = str(resolution.split('x')[0]) + "x" + str(resolution.split('x')[1])

            out = {
                "brand": properties["ro.product.brand"],
                "android_version": properties["ro.build.version.release"],
                "manufacturer": properties["ro.product.manufacturer"],
                "resolution_ratio": properties["resolution"]
            }
            return out, None
        except subprocess.CalledProcessError as e:
            return None, str(e)

    @staticmethod
    def get_screenshot_catalog_path(file_dir: str, file_name: str) -> str | Path:
        root_path = PathUtil.get_current_file_absolute_path(__file__).parent.parent
        return str(root_path.joinpath(file_dir).joinpath(file_name))

    @staticmethod
    def screen_cap(device):
        """截屏"""
        AdbUtil.run_shell_command(f"adb -s {device} shell screencap /sdcard/screenshot.png")

    @staticmethod
    def screen_cap_pull(device):
        """拉取截屏图片"""
        screenshot_name = f"{device}_screen.png"
        screenshot_path = AdbUtil.get_screenshot_catalog_path(ADVERTISING_SCREENSHOT, screenshot_name)
        AdbUtil.run_shell_command(f"adb -s {device} pull /sdcard/screenshot.png {screenshot_path}")
        return screenshot_path

    @staticmethod
    def screen_cap_delete(device):
        """删除截屏图片"""
        AdbUtil.run_shell_command(f"adb -s {device} shell rm /sdcard/screenshot.png")

    # @staticmethod
    # def delete_photo(device: str, specify_image: str) -> None:
    #     """
    #     删除指定位置指定名字的图片
    #
    #     :param device: 设备id
    #     :param specify_image:  待删除的手机图片，该字符串包含图片路径和图片名称
    #     :return:
    #     """
    #     AdbUtil.run_shell_command(f"adb -s {device} shell rm {specify_image}")

    # @staticmethod
    # def store_photo(device: str, c_workspace_path: str, photo_relative_path, specify_image) -> None:
    #     """将电脑端图片储存到手机端指定位置"""
    #     AdbUtil.run_shell_command(f"adb -s {device} push {c_workspace_path}/{photo_relative_path} {specify_image}")

    @staticmethod
    def stop_app(device: str, app_package: str):
        """
        根据设备id和app包名停止指定设备上的app

        :param device: 设备id
        :param app_package: 软件包名
        :return:
        """
        AdbUtil.run_shell_command(f"adb -s {device} shell am force-stop {app_package}")

    @staticmethod
    def back_home(device):
        """返回主页"""
        AdbUtil.run_shell_command(f"adb -s {device} shell input keyevent KEYCODE_HOME")

    @staticmethod
    def back(device):
        """返回上一页"""
        AdbUtil.run_shell_command(f"adb -s {device} shell input keyevent KEYCODE_BACK")

    @staticmethod
    def swipe(device, start_position, end_position, duration=100):
        """滑动"""
        AdbUtil.run_shell_command(
            f"adb -s {device} shell input swipe "
            f"{start_position[0]} {start_position[1]} "
            f"{end_position[0]} {end_position[1]} "
            f"{duration}"
        )

    @staticmethod
    def click(device, x, y):
        """点击"""
        AdbUtil.run_shell_command(f"adb -s {device} shell input tap {x} {y}")

    @staticmethod
    def reboot_machine(device: str) -> None:
        """
        根据设备id 重启设备

        :param device:
        :return:
        """
        AdbUtil.run_shell_command(f"adb -s {device} reboot")

    @staticmethod
    def change_volume(device: str, action_: int) -> None:
        """
        传入设备id和动作 升高或者降低手机音量

        :param device:
        :param action_:  控制手机音量行为 1为升高手机音量，0为降低手机音量
        :return:
        """
        if action_:
            # 降低手机音量
            AdbUtil.run_shell_command(f"adb -s {device} shell input keyevent 25")
        else:
            # 升高手机音量
            AdbUtil.run_shell_command(f"adb -s {device} shell input keyevent 24")

    @staticmethod
    def change_luminance(device: str, action_: int) -> None:
        """
        传入设备id 调节手机亮度

        :param device:
        :param action_: 两个可选值1/0  1: 表示提升手机亮度  0: 表示降低手机亮度
        :return:
        """
        if action_:
            # 提高手机亮度
            AdbUtil.run_shell_command(f"adb -s {device} shell input keyevent 220")
        else:
            # 降低手机亮度
            AdbUtil.run_shell_command(f"adb -s {device} shell input keyevent 221")

    @staticmethod
    def slince_device(device: str) -> None:
        """
        指定设备静音

        :param device:
        :return:
        """
        AdbUtil.run_shell_command(f"adb -s {device} shell input keyevent 164")

    @staticmethod
    def install_apk(device: str, apk_path: str) -> None:
        """
        安装储存到本地设备的apk包

        :return:
        """
        AdbUtil.run_shell_command(f"adb -s {device} install -r {apk_path}")

    @staticmethod
    def is_access_internet(device: str):
        """
        判断设备是否通网

        :return:
        """
        result = AdbUtil.run_shell_command(f"adb -s {device} shell ping -c 1 www.baidu.com")
        if result[0] is None:
            return 0
        else:
            return 1

    @staticmethod
    def notice_which_device(device: str) -> None:
        """
        输入设备id 对应设备进入 关于手机 界面

        :param device:
        :return:
        """
        AdbUtil.run_shell_command(f"adb -s {device} shell am start -a android.settings.DEVICE_INFO_SETTINGS")

    @staticmethod
    def del_app_package(device_id: str, package_name: str) -> None:
        """
        根据device_id和package_name删除app

        :param device_id:
        :param package_name:
        :return:
        """
        AdbUtil.run_shell_command(f"adb -s {device_id} uninstall {package_name}")

    @staticmethod
    def input_text(device_id: str, input_text: str) -> None:
        """
        在焦点聚焦处输入文字

        :param device_id:
        :param input_text:
        :return:
        """
        AdbUtil.run_shell_command(f"adb -s {device_id} shell input text {input_text}")

    @staticmethod
    def skip_to_app_page(app_package_name: str) -> None:
        """
        更具app的包名, 跳转到指定app的app market download page

        :param app_package_name:
        :return:
        """
        AdbUtil.run_shell_command(
            f'adb shell am start -a android.intent.action.VIEW -d "market://details?id={app_package_name}"')
