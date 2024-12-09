#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/9/28 16:20
# @Author : limber
# @desc :


from store_service.mapper.device_mapper import DeviceMapper
from store_service.model.model_device import Device
from typing import List, Optional


class DeviceService:
    def select(self, online_state="all", task_state="all") -> List[Device]:
        """
        条件查询符合条件的设备

        :param online_state: 可选值all, online, offline
        :param task_state: 可选值all, yes, no
        :return:
        """
        online_state_table = {"all": "", "online": 1, "offline": 0}
        task_state_table = {"all": "", "yes": 1, "no": 0}

        online_state_code = online_state_table[online_state]
        task_state_code = task_state_table[task_state]

        # 1、查询全部设备
        device_list = DeviceMapper().select_all()

        # 2、根据条件筛选设备
        suitable_device_list = []
        for device_ in device_list:
            condition_one = online_state_code == "" or online_state_code == device_.online_state
            condition_two = task_state_code == "" or task_state_code == device_.task_state
            if condition_one and condition_two:
                suitable_device_list.append(device_)

        # 3、返回符合条件的设备
        return suitable_device_list

    def select_page(self, page_number: int, items_: int, online_state="all", task_state="all"):
        """
        根据条件分页获取设备

        :param page_number:
        :param items_:
        :param online_state:
        :param task_state:
        :return:
        """
        online_state_table = {"all": "", "online": 1, "offline": 0}
        task_state_table = {"all": "", "yes": 1, "no": 0}

        online_state_code = online_state_table[online_state]
        task_state_code = task_state_table[task_state]

        # 1、查询全部设备
        device_list = DeviceMapper().select_all()

        # 2、根据条件筛选设备
        suitable_device_list = []
        for device_ in device_list:
            condition_one = online_state_code == "" or online_state_code == device_.online_state
            condition_two = task_state_code == "" or task_state_code == device_.task_state
            if condition_one and condition_two:
                suitable_device_list.append(device_)
        offset_item = page_number * items_
        last_data_index = offset_item + items_
        # 该分页无数据
        if len(suitable_device_list) <= offset_item:
            return []
        # 该分页数据达不到每页显示数据条数
        elif offset_item < len(suitable_device_list) < last_data_index:
            return suitable_device_list[offset_item:]
        else:
            return suitable_device_list[offset_item:last_data_index]

    def select_count_page(self, items_: int, online_state="all", task_state="all"):
        """
        条件查询符合条件的设备

        :param online_state: 可选值all, online, offline
        :param task_state: 可选值all, yes, no
        :return:
        """
        online_state_table = {"all": "", "online": 1, "offline": 0}
        task_state_table = {"all": "", "yes": 1, "no": 0}

        online_state_code = online_state_table[online_state]
        task_state_code = task_state_table[task_state]

        # 1、查询全部设备
        device_list = DeviceMapper().select_all()

        # 2、根据条件筛选设备
        suitable_device_list = []
        for device_ in device_list:
            condition_one = online_state_code == "" or online_state_code == device_.online_state
            condition_two = task_state_code == "" or task_state_code == device_.task_state
            if condition_one and condition_two:
                suitable_device_list.append(device_)

        # 3、返回符合条件的设备
        return len(suitable_device_list) // items_ + 1

    def delete(self, id):
        # 根据传入的id删除对应设备
        DeviceMapper().delete_by_id(id)

    def select_by_device_id(self, device_id: str) -> Optional[Device]:
        result = DeviceMapper().select_by_device_id(device_id)
        if result is not None:
            return result
        return None

    def add_device(self, device: Device) -> None:
        DeviceMapper().insert(device)

    def update(self, device: Device) -> None:
        DeviceMapper().update(device)

    # ##################以上是旧的群控版本查询设备api###################

    def select_condition_device_list(self,
                                     page_number=0,
                                     total_item=15,
                                     task_status: Optional[int] = None,
                                     online_status: Optional[int] = None
                                     ):
        """
        分页条件查询

        :param page_number: 页数
        :param total_item: 单页数据条数
        :param task_status: 任务状态
        :param online_status: 在线状态
        :return:
        """
        sql_ = (f"select * from tb_device "
                f"where task_status={task_status} and online_status={online_status} "
                f"limit {total_item} offset {page_number * total_item}"
                )

        result = DeviceMapper().select_specific_devices(sql_)
        return result

    def select_device_list(self,
                           page_number=0,
                           total_item=15):
        sql_ = (f"select * from tb_device "
                f"limit {total_item} offset {page_number * total_item}"
                )

        result = DeviceMapper().select_specific_devices(sql_)
        return result

    def select_online_state_devices(self, online_status: int) -> List[Device]:
        all_devices = DeviceMapper().select_all()
        suitable_devices = []
        for device_ in all_devices:
            if device_.online_state == online_status:
                suitable_devices.append(device_)
        return suitable_devices

    def select_all_devices(self):
        all_devices = DeviceMapper().select_all()
        return all_devices



if __name__ == '__main__':
    pass
    # result = DeviceService().select("offline", "all")
    # for i in result:
    #     print(i)
    # result = DeviceService().select_page(4, 2)
    # print(result)
    # result = DeviceService().select_count()
    # print(result)
