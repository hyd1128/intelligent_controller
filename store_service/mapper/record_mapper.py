#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/9/27 11:19
# @Author : limber
# @desc :


from store_service.connection_pool import ConnectionPool
from store_service.model.model_record import Record
from typing import Optional, List


class RecordMapper:
    """
    脚本代理类
    """

    def __init__(self):
        self.pool = ConnectionPool
        self.conn = self.pool.get_connection()
        self.cursor = self.conn.cursor()

    def select_by_id(self, record_id: int) -> Optional[Record]:
        """
        通过id查找记录

        :param record_id:
        :return:
        """
        id_ = record_id
        sql_ = "select * from tb_record where id = ? and deleted != 1;"
        params = (id_,)
        result = self.cursor.execute(sql_, params).fetchone()
        self.pool.return_connection(self.conn)

        if result is not None:
            return Record(*result)
        return result

    def select_record(self, device_id: str, task_name: str, date: str) -> Optional[Record]:
        """
        根据设备id、任务名称、日期查询记录,正常情况下符合条件的记录不超过一条

        :param device_id:
        :param task_name:
        :param date:
        :return:
        """

        params = (device_id, task_name, date)
        sql_ = "select * from tb_record where device_id=? and task_name=? and date=? and deleted != 1;"
        result = self.cursor.execute(sql_, params).fetchone()
        self.pool.return_connection(self.conn)

        if result:
            return Record(*result)
        return result

    def select_record_two(self, device_id: str, date: str) -> List[Record]:
        """
        根据设备id、任务名称、日期查询记录,正常情况下符合条件的记录不超过一条

        :param device_id:
        :param task_name:
        :param date:
        :return:
        """

        params = (device_id, date)
        sql_ = "select * from tb_record where device_id=? and date=? and deleted != 1;"
        result = self.cursor.execute(sql_, params).fetchall()
        self.pool.return_connection(self.conn)
        if result:
            script_list_ = []
            for script_ in result:
                script_list_.append(Record(*script_))
            return script_list_
        return result


    def select_all(self) -> List[Record]:
        """
        查询全部任务

        :return:
        """

        sql_ = "select * from tb_record where deleted != 1"
        result = self.cursor.execute(sql_).fetchall()
        self.pool.return_connection(self.conn)
        if result:
            script_list_ = []
            for script_ in result:
                script_list_.append(Record(*script_))
            return script_list_
        return result

    def select_count(self):
        """
        查询该表总数据条数

        :return:
        """
        sql_ = "select count(*) from tb_record;"
        try:
            self.cursor.execute(sql_)
            return self.cursor.fetchone()[0]
        except Exception as e:
            print(str(e))
        finally:
            self.pool.return_connection(self.conn)

    def select_page(self, per_page_item: int, page_number: int) -> List[Record]:
        """
        分页插叙方法
        根据传递过来的单页显示数据条数和偏移量获得查询页数据

        :param per_page_item: 单页显示条数
        :param page_number: 偏移页数
        :return:
        """
        # 偏移量
        offset_ = page_number * per_page_item
        params = (per_page_item, offset_)
        sql_ = "select * from tb_record where deleted = 0 order by id desc limit ? offset ?"
        try:
            result = self.cursor.execute(sql_, params).fetchall()
            if result:
                suitable_list_ = []
                for record_ in result:
                    suitable_list_.append(Record(*record_))
                return suitable_list_
            return result
        except Exception as e:
            print(str(e))
        finally:
            self.pool.return_connection(self.conn)

    def insert(self, record: Record) -> int:
        """
        插入一条记录

        :param record:
        :return:
        """
        params = (record.device_id, record.task_name, record.execution_times, record.today_execution_time,
                  record.date, record.deleted, record.specify_device_execution_times, record.task_last_execution_time
                  , record.today_end_execution_time)
        sql_ = ("insert into tb_record "
                "(device_id, task_name, execution_times, today_execution_time, date, "
                "deleted, specify_device_execution_times, task_last_execution_time"
                ", today_end_execution_time) "
                "values (?, ?, ?, ?, ?, ?, ?, ?, ?)")
        try:
            self.cursor.execute(sql_, params)
            self.conn.commit()
            return self.cursor.rowcount
        except Exception as e:
            print(str(e))
            self.conn.rollback()
        finally:
            self.pool.return_connection(self.conn)

    def update(self, record: Record) -> int:
        """
        更新记录

        :param record:
        :return:
        """

        params = record.to_dict()
        sql_ = (f"update tb_record set "
                f"device_id=:device_id, task_name=:task_name, execution_times=:execution_times, "
                f"today_execution_time=:today_execution_time, date=:date, deleted=:deleted,"
                f"specify_device_execution_times=:specify_device_execution_times,"
                f"task_last_execution_time=:task_last_execution_time,"
                f"today_end_execution_time=:today_end_execution_time"
                f" where id = {record.id}")

        try:
            self.cursor.execute(sql_, params)
            self.conn.commit()
            return self.cursor.rowcount
        except Exception as e:
            print(str(e))
            self.conn.rollback()
        finally:
            self.pool.return_connection(self.conn)

    def delete_logiclly(self, device_id: str, task_name: str, date: str):
        """
        逻辑删除记录

        :param device_id:
        :param task_name:
        :param date:
        :return:
        """
        params = (device_id, task_name, date)
        sql_ = "update tb_record set deleted=1 where device_id=? and task_name=? and date=?;"
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


if __name__ == "__main__":
    pass
    # record_info_1 = {
    #     "device_id": "abcd",
    #     "task_name": "prism_task_1",
    #     "execution_times": 5,
    #     "today_execution_time": "08:00:00",
    #     "date": "2024-9-28"
    # }

    # 添加一条记录
    # record_obj = Record(**record_info_1)
    # result = RecordMapper().insert(record_obj)
    # print(result)

    # # 根据device_id, task_name, date查询记录
    # device_id_ = "abc"
    # task_name = "prism_task_1"
    # date = "2024-9-28"
    # result = RecordMapper().select_record(device_id_, task_name, date)
    # print(result)

    # 查询全部
    # result = RecordMapper().select_all()
    # for i in result:
    #     print(i)

    # 更新
    # record_update = result
    # print(record_update)
    # record_update.execution_times += 1
    # print(record_update)
    # result = RecordMapper().update(record_update)
    # print(result)

    # 逻辑删除一条记录
    # device_id = "abcd"
    # task_name = "prism_task_1"
    # date = "2024-9-28"
    # result = RecordMapper().delete_logiclly(device_id, task_name, date)
    # print(result)

    # 测试查询总条数功能
    # result = RecordMapper().select_count()
    # print(result)

    # 测试分页查询功能
    # per_page_number = 15
    # page_number = 2
    #
    # total_number = RecordMapper().select_count()
    # total_page = total_number // per_page_number + 1
    #
    # if page_number < total_page:
    #     result = RecordMapper().select_page(per_page_number, page_number)
    #     for i in result:
    #         print(i)
    # else:
    #     print("当前页数已超过总页数")
