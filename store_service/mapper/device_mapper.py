#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/9/27 11:18
# @Author : limber
# @desc : device代理类

from store_service.connection_pool import ConnectionPool
from store_service.model.model_device import Device
from typing import Optional, List


class DeviceMapper:
    """
    设备代理类
    """

    def __init__(self):
        self.pool = ConnectionPool
        self.conn = self.pool.get_connection()
        self.cursor = self.conn.cursor()

    def select_by_id(self, id_: int) -> Optional[Device]:
        """
        通过id查找设备

        :param id_:
        :return:
        """
        sql_ = "select * from tb_device where id = ?;"
        params = (id_,)
        result = self.cursor.execute(sql_, params).fetchone()
        self.pool.return_connection(self.conn)

        if result is not None:
            return Device(*result)
        return result

    def select_by_device_id(self, device_id: str) -> Optional[Device]:
        """
        通过device_id查找设备

        :param device_id:
        :return:
        """
        id_ = device_id
        sql_ = "select * from tb_device where device_id = ?;"
        params = (id_,)
        result = self.cursor.execute(sql_, params).fetchone()
        self.pool.return_connection(self.conn)

        if result is not None:
            return Device(*result)
        return result

    def select_all(self) -> List[Device]:
        """
        查询全部的设备

        :return:
        """
        sql_ = "select * from tb_device;"
        result = self.cursor.execute(sql_).fetchall()
        self.pool.return_connection(self.conn)
        if result:
            device_list_ = []
            for device_ in result:
                device_list_.append(Device(*device_))
            return device_list_
        return result

    def select_specific_devices(self, sql_: str) -> List[Device]:
        """
        条件查询符合条件的设备

        :param sql_:
        :return:
        """
        result = self.cursor.execute(sql_).fetchall()
        self.pool.return_connection(self.conn)
        if result:
            device_list_ = []
            for device_ in result:
                device_list_.append(Device(*device_))
            return device_list_
        return result

    def insert(self, device: Device) -> int:
        """
        添加设备

        :param device:
        :return:
        """
        params = (device.device_id,
                  device.brand,
                  device.manufacturer,
                  device.android_version,
                  device.resolution_ratio,
                  device.online_state,
                  device.task_state, device.coord,
                  device.locating_app_status,
                  device.locating_app_last_reload_time
                  )

        sql_ = ("insert into tb_device "
                "(device_id, "
                "brand, "
                "manufacturer, "
                "android_version, "
                "resolution_ratio, "
                "online_state, "
                "task_state, "
                "coord, "
                "locating_app_status, "
                "locating_app_last_reload_time"
                ") "
                "values (?, ?, ?, ? , ?, ?, ?, ?, ?, ?)")
        try:
            self.cursor.execute(sql_, params)
            self.conn.commit()
            return self.cursor.rowcount
        except Exception as e:
            print(str(e))
            self.conn.rollback()
        finally:
            self.pool.return_connection(self.conn)

    def delete_by_id(self, id_) -> int:
        """
        根据id删除设备

        :param id_:
        :return:
        """
        params = (id_,)
        sql_ = "delete from tb_device where id = ?"
        try:
            self.cursor.execute(sql_, params)
            self.conn.commit()
            return self.cursor.rowcount
        except Exception as e:
            print(str(e))
            self.conn.rollback()
        finally:
            self.pool.return_connection(self.conn)

    def update(self, device: Device) -> int:
        """
        根据id更新设备

        :param device:
        :return:
        """
        params = device.to_dict()
        sql_ = (f"update tb_device set "
                f"device_id=:device_id, "
                f"brand=:brand, "
                f"manufacturer=:manufacturer, "
                f"android_version=:android_version, "
                f"resolution_ratio=:resolution_ratio, "
                f"online_state=:online_state, "
                f"task_state=:task_state, "
                f"coord=:coord, "
                f"locating_app_status=:locating_app_status, "
                f"locating_app_last_reload_time=:locating_app_last_reload_time "
                f"where id={device.id}"
                )

        try:
            self.cursor.execute(sql_, params)
            self.conn.commit()
            return self.cursor.rowcount
        except Exception as e:
            print(str(e))
            self.conn.rollback()
        finally:
            self.pool.return_connection(self.conn)

    def dqm_script(self, sql_):
        """
        传入sql执行dql语句

        :param sql_:
        :return:
        """
        pass

    def dml_script(self, sql_):
        """
        传入sql执行dml语句

        :param sql_:
        :return:
        """
        pass


if __name__ == '__main__':
    pass

    # 添加单个
    # device_1 = {"device_id": "2345", "brand": "sanxing", "android_version": 14, "task_state": 0}
    # device = Device(**device_1)
    # result = DeviceMapper().insert(device)
    # print(result)

    device_1 = {"device_id": "2345",
                "brand": "sanxing",
                "manufacturer": "sanxing",
                "android_version": 14,
                "resolution_ratio": "999x888",
                "online_state": 1,
                "task_state": 0,
                "coord": "[33, 66]",
                "locating_app_status": 0}
    device = Device(**device_1)
    result = DeviceMapper().insert(device)
    print(result)

    # # 查询全部
    # result = DeviceMapper().select_all()
    # print(result)
    # print(result[0])

    # # 查单个
    # result = DeviceMapper().select_by_id(6)
    # print(result)

    # 删除
    # result = DeviceMapper().delete_by_id(4)
    # print(result)

    # # 更新
    # result.brand = "MEIZU"
    # result = DeviceMapper().update(result)
    # print(result)
