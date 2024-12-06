import subprocess
# from logger_zk.logger_types import logger_run
from typing import Any


# 命令
# 设备列表：adb devices
# 品牌：adb -s [设备号] shell getprop ro.product.brand
# Android版本号：adb -s [设备号] shell getprop ro.build.version.release
# 厂商：adb -s [设备号] shell getprop ro.product.manufacturer
# 分辨率：adb -s [设备号] shell wm size
# 点击：adb -s [设备号] shell input tap [x坐标] [y坐标]
# 返回主页：adb -s [设备号] shell input keyevent KEYCODE_HOME
# 返回上一页：adb -s [设备号] shell input keyevent KEYCODE_BACK
# 上下左右滑动：adb -s [设备号] shell input swipe [起点x坐标] [起点y坐标] [终点x坐标] [终点y坐标] [时间]
# 截屏：adb -s [设备号] shell screencap /sdcard/screenshot.png
# 拉取图片到本地：sudo adb -s [设备号] pull /sdcard/screenshot.png [本地路径]
# 删除截屏：adb -s [设备号] shell rm /sdcard/screenshot.png


def run_command(command):
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
            # logger_run.error(f"run adb command appear Error: {result.stderr}")
            return None, result.stderr
        return result.stdout, None
    except subprocess.CalledProcessError as e:
        # logger_run.error(f"Command '{command}' returned non-zero exit status {e.returncode}.")
        # logger_run.error(f"Output: {e.stdout}")
        # logger_run.error(f"Error++: {e.stderr}")
        return None, e.stderr


def device_list():
    """
    获取设备列表

    示例: ['192.168.31.182:37651']
    """
    devices, err = run_command("adb devices")
    if err:
        return None, err
    lines = devices.strip().split('\n')
    device_lines = lines[1:]
    devices = [line.split()[0] for line in device_lines if line.strip()]
    return devices, None


def info(device):
    """获取手机的品牌、 android版本号、厂商、分辨率"""

    # 品牌、Android版本号、厂商
    try:
        result, err = run_command(f"adb -s {device} shell getprop")
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
        result, err = run_command(f"adb -s {device} shell wm size")
        if err:
            return None, err
        for line in result.strip().split('\n'):
            if "Physical size" in line:
                resolution = line.split(": ")[1].strip()
                properties["resolution"] = str(resolution.split('x')[0]) + "x" + str(resolution.split('x')[1])

        # logger_run.info(f"品牌: {properties['ro.product.brand']}")
        # logger_run.info(f"Android版本号: {properties['ro.build.version.release']}")
        # logger_run.info(f"厂商: {properties['ro.product.manufacturer']}")
        # logger_run.info(f"分辨率: {properties['resolution']}")

        out = {
            "brand": properties["ro.product.brand"],
            "android_version": properties["ro.build.version.release"],
            "manufacturer": properties["ro.product.manufacturer"],
            "resolution_ratio": properties["resolution"]
        }
        return out, None
    except subprocess.CalledProcessError as e:
        return None, e


def screen_cap(device):
    """截屏"""
    run_command(f"adb -s {device} shell screencap /sdcard/screenshot.png")


def screen_cap_pull(device):
    """拉取截屏图片"""
    run_command(f"adb -s {device} pull /sdcard/screenshot.png ./screens/{device}_screen.png")
    return f"./screens/{device}_screen.png"


def screen_cap_delete(device):
    """删除截屏图片"""
    run_command(f"adb -s {device} shell rm /sdcard/screenshot.png")


#
def delete_photo(device: str, specify_image: str) -> None:
    """
    删除指定位置指定名字的图片

    :param device: 设备id
    :param specify_image:  待删除的手机图片，该字符串包含图片路径和图片名称
    :return:
    """
    run_command(f"adb -s {device} shell rm {specify_image}")


def store_photo(device: str, c_workspace_path: str, photo_relative_path, specify_image) -> None:
    """将电脑端图片储存到手机端指定位置"""
    run_command(f"adb -s {device} push {c_workspace_path}/{photo_relative_path} {specify_image}")


def stop_app(device: str, app_package: str):
    """adb强制停止一个应用程序"""
    run_command(f"adb -s {device} shell am force-stop {app_package}")


def back_home(device):
    """返回主页"""
    run_command(f"adb -s {device} shell input keyevent KEYCODE_HOME")


def back(device):
    """返回上一页"""
    run_command(f"adb -s {device} shell input keyevent KEYCODE_BACK")


def swipe(device, start_position, end_position, duration=100):
    """滑动"""
    run_command(
        f"adb -s {device} shell input swipe "
        f"{start_position[0]} {start_position[1]} "
        f"{end_position[0]} {end_position[1]} "
        f"{duration}"
    )


def click(device, x, y):
    """点击"""
    run_command(f"adb -s {device} shell input tap {x} {y}")


def reboot_machine(device: str) -> None:
    """
    根据设备id 重启设备

    :param device:
    :return:
    """
    run_command(f"adb -s {device} reboot")


def change_volume(device: str, action_: str) -> None:
    """
    传入设备id和动作 升高或者降低手机音量

    :param device:
    :param action_:  控制手机音量行为 rise为升高手机音量，fall为降低手机音量
    :return:
    """
    if action_ == "rise":
        # 降低手机音量
        run_command(f"adb -s {device} shell input keyevent 25")
    else:
        # 升高手机音量
        run_command(f"adb -s {device} shell input keyevent 24")


def change_luminance(device: str, action_: str) -> None:
    """
    传入设备id 调节手机亮度

    :param device:
    :param action_: 两个可选值 rise/fall  rise: 表示提升手机亮度  fall: 表示降低手机亮度
    :return:
    """
    if action_ == "rise":
        # 提高手机亮度
        run_command(f"adb -s {device} shell input keyevent 220")
    else:
        # 降低手机亮度
        run_command(f"adb -s {device} shell input keyevent 221")


def slince_device(device: str) -> None:
    """
    指定设备静音

    :param device:
    :return:
    """
    run_command(f"adb -s {device} shell input keyevent 164")


def install_apk(device: str, apk_path: str) -> str:
    """
    安装储存到本地设备的apk包

    :return:
    """
    run_command(f"adb -s {device} install -r {apk_path}")


def is_access_internet(device: str):
    """
    判断设备是否通网

    :return:
    """
    result = run_command(f"adb -s {device} shell ping -c 1 www.baidu.com")
    if result[0] is None:
        return 0
    else:
        return 1


def notice_which_device(device: str) -> None:
    """
    输入设备id 对应设备进入 关于手机 界面

    :param device:
    :return:
    """
    run_command(f"adb -s {device} shell am start -a android.settings.DEVICE_INFO_SETTINGS")


def del_app_package(device_id: str, package_name: str) -> None:
    """
    确定device id 和 包名，删除app

    :param device_id:
    :param package_name:
    :return:
    """
    run_command(f"adb -s {device_id} uninstall {package_name}")


def input_text(device_id: str, input_text: str) -> None:
    """
    在焦点聚焦处输入文字

    :param device_id:
    :param input_text:
    :return:
    """
    run_command(f"adb -s {device_id} shell input text {input_text}")


if __name__ == '__main__':
    result = is_access_internet('R5CN90H2FVX')
    if result:
        print("设备已联网")
    else:
        print("设备未联网")
