#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/9/27 11:19
# @Author : limber
# @desc :


from store_service.connection_pool import ConnectionPool
from store_service.model.model_task import Task
from typing import Optional, List


class TaskMapper:
    """
    脚本代理类
    """

    def __init__(self):
        self.pool = ConnectionPool
        self.conn = self.pool.get_connection()
        self.cursor = self.conn.cursor()

    def select_by_id(self, task_id: int) -> Optional[Task]:
        """
        根据id查找任务

        :param task_id:
        :return:
        """
        id_ = task_id
        sql_ = "select * from tb_task where id = ?;"
        params = (id_,)
        result = self.cursor.execute(sql_, params).fetchone()
        self.pool.return_connection(self.conn)

        if result is not None:
            return Task(*result)
        return result

    def select_by_date(self, date_: str) -> List[Task]:
        """
        根据日期查找task任务

        :param date_:
        :return:
        """

        task_release_date = date_
        sql_ = "select * from tb_task where task_release_date = ?;"
        params = (task_release_date,)
        result = self.cursor.execute(sql_, params).fetchall()
        self.pool.return_connection(self.conn)

        if result:
            task_list_ = []
            for task_ in result:
                task_list_.append(Task(*task_))
            return task_list_
        return result

    def select_all(self) -> List[Task]:
        """
        查询全部任务

        :return:
        """
        sql_ = "select * from tb_task"
        result = self.cursor.execute(sql_).fetchall()
        self.pool.return_connection(self.conn)
        if result:
            task_list_ = []
            for task_ in result:
                task_list_.append(Task(*task_))
            return task_list_
        return result

    def insert(self, task: Task) -> int:
        """
        插入一个新任务

        :param task:
        :return:
        """

        params = (task.task_name, task.task_execution_duration, task.min_execution_times,
                  task.max_execution_times, task.task_release_date, task.app)

        sql_ = ("insert into tb_task "
                "(task_name, task_execution_duration, min_execution_times, "
                "max_execution_times, task_release_date, app) "
                "values (?, ?, ?, ?, ?, ?)")
        try:
            self.cursor.execute(sql_, params)
            self.conn.commit()
            return self.cursor.rowcount
        except Exception as e:
            print(str(e))
            self.conn.rollback()
        finally:
            self.pool.return_connection(self.conn)

    def delete_by_name(self, task_name) -> int:
        """
        根据任务名称删除任务

        :param task_name:
        :return:
        """

        params = (task_name,)
        sql_ = "delete from tb_task where task_name = ?"
        try:
            self.cursor.execute(sql_, params)
            self.conn.commit()
            return self.cursor.rowcount
        except Exception as e:
            print(str(e))
            self.conn.rollback()
        finally:
            self.pool.return_connection(self.conn)

    def update(self, task: Task) -> int:
        """
        更新Task任务

        当前业务暂未使用到更新
        :param task:
        :return:
        """
        pass

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
    from datetime import time, datetime, date
    # # 创建任务的持续时长
    # duration_time = time(8, 0, 0).strftime("%H:%M:%S")
    # # 创建任务的发布日期
    # task_release_date =datetime.now().strftime("%Y-%m-%d")
    # task_info_1 = {"task_name": "innova_task_2", "task_execution_duration": duration_time,
    #                "min_execution_times": 5, "max_execution_times": 10,
    #                "task_release_date": task_release_date, "app": "innova"}
    #
    # task_obj_1 = Task(**task_info_1)
    # print(task_obj_1)

    # 添加一个task任务
    # result = TaskMapper().insert(task_obj_1)
    # print(result)

    # 根据日期查询任务集
    # date = date(2024, 9, 28).strftime("%Y-%m-%d")
    # print(date)
    # result = TaskMapper().select_by_date(date)
    # for i in result:
    #     print(i)

    # # 根据任务名称删除app
    # task_name = "prism_task_1"
    # result = TaskMapper().delete_by_name(task_name)
    # print(result)



