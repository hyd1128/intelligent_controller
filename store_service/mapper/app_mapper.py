#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/9/27 11:18
# @Author : limber
# @desc :

from store_service.connection_pool import ConnectionPool
from store_service.model.model_app import App
from typing import Optional, List


class AppMapper:
    """
    设备代理类
    """

    def __init__(self):
        self.pool = ConnectionPool
        self.conn = self.pool.get_connection()
        self.cursor = self.conn.cursor()

    def select_by_id(self, app_id: int) -> Optional[App]:
        """
        通过id查找app

        :param app_id:
        :return:
        """
        id_ = app_id
        sql_ = "select * from tb_app where id = ?;"
        params = (id_,)
        result = self.cursor.execute(sql_, params).fetchone()
        self.pool.return_connection(self.conn)

        if result is not None:
            return App(*result)
        return result

    def select_by_name(self, app_name: str) -> Optional[App]:
        """
        根据app的名称查找app

        :param app_name:
        :return:
        """
        app_name = app_name
        sql_ = "select * from tb_app where app = ?;"
        params = (app_name,)
        result = self.cursor.execute(sql_, params).fetchone()
        self.pool.return_connection(self.conn)

        if result is not None:
            return App(*result)
        return result

    def select_all(self) -> List[App]:
        """
        查询全部app

        :return:
        """
        sql_ = "select * from tb_app"
        result = self.cursor.execute(sql_).fetchall()
        self.pool.return_connection(self.conn)
        if result:
            app_list_ = []
            for app_ in result:
                app_list_.append(App(*app_))
            return app_list_
        return result

    def insert(self, app: App) -> int:
        """
        插入一款app软件

        :param app:
        :return:
        """
        params = (app.app, )
        sql_ = "insert into tb_app (app) values (?)"
        try:
            self.cursor.execute(sql_, params)
            self.conn.commit()
            return self.cursor.rowcount
        except Exception as e:
            print(str(e))
            self.conn.rollback()
        finally:
            self.pool.return_connection(self.conn)

    def delete_by_name(self, name) -> int:
        """
        根据app名称删除app

        :param name:
        :return:
        """
        params = (name, )
        sql_ = """delete from tb_app where app = ?"""
        try:
            self.cursor.execute(sql_, params)
            self.conn.commit()
            return self.cursor.rowcount
        except Exception as e:
            print(str(e))
            self.conn.rollback()
        finally:
            self.pool.return_connection(self.conn)

    def update(self, app: App) -> int:
        """
        根据id删除app

        :param app:
        :return:
        """

        params = app.to_dict()
        sql_ = f"update tb_app set app = :app where id = {app.id}"

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

    # app_info_1 = {"app_name": "prism"}
    # app_info_2 = {"app_name": "innova"}
    # app1 = App(**app_info_1)
    # app2 = App(**app_info_2)
    # print(app1)
    # print(app2)
    # app_list = [app1, app2]
    # # 添加数据
    # for i in app_list:
    #     result = AppMapper().insert(i)
    #     print(f"添加了{result}条数据")

    # 根据name查询单个数据
    # result = AppMapper().select_by_name("prism")
    # print(result)

    # 查询全部数据
    # result = AppMapper().select_all()
    # print(result[0])
    # print(result[1])

    # 更新数据
    # prism_app = result
    # prism_app.app = "twitter"
    # result = AppMapper().update(prism_app)
    # print(result)

    # 删除数据
    # result = AppMapper().delete_by_name("innova")
    # print(result)
