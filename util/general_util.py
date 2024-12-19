#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/19 16:25
# @Author : limber
# @desc :
import random
from typing import List


class GeneralUtil:
    @staticmethod
    def generate_coordinate(coord_1, coord_2) -> List[float]:
        """
        采用GCJ02坐标系，实用于高德地图，微信地图由于该查询坐标接口支持小数点后六位查询，
        所以在生成新坐标前将每一个坐标扩大1000000，使用新坐标的时候再缩小1000000

        :param coord_1: 坐标1
        :param coord_2: 坐标2
        :return:
        """
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
