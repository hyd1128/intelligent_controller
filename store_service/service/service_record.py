#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/9/28 16:20
# @Author : limber
# @desc :

from store_service.mapper.record_mapper import RecordMapper
from store_service.model.model_record import Record
from typing import List


class RecordService:

    def select_all(self, device_id: str = "", task_name: str = "", date: str = "") -> List[Record]:
        # 1、查询全部记录
        record_list = RecordMapper().select_all()

        # 2、筛选符合条件的记录
        suitable_record_list = []
        for record_ in record_list:
            condition_one = device_id == "" or record_.device_id == device_id
            condition_two = task_name == "" or record_.task_name == task_name
            condition_three = date == "" or record_.date == date
            if condition_one and condition_two and condition_three:
                suitable_record_list.append(record_)

        # 返回符合条件的记录
        return suitable_record_list

    def select_record(self, device_id, task_name, date):
        suitable_record = RecordMapper().select_record(device_id, task_name, date)
        return suitable_record

    def select_record_two(self, device_id, date):
        suitable_record = RecordMapper().select_record_two(device_id, date)
        return suitable_record

    def get_total_page(self, per_page_item: int) -> int:
        """
        获得总页数

        :param per_page_item:
        :return:
        """

        total_number_count = RecordMapper().select_count()
        total_page = total_number_count // per_page_item + 1
        return total_page

    def select_page_data(self, per_page_item: int, page_number: int) -> List[Record]:
        """
        获取分页数据

        :param per_page_item:
        :param page_number:
        :return:
        """
        result_ = RecordMapper().select_page(per_page_item, page_number)
        return result_

    def add_record(self, record: Record) -> None:
        RecordMapper().insert(record)

    def update_record(self, record: Record) -> None:
        RecordMapper().update(record)
