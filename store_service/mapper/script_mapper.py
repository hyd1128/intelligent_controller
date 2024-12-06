#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/9/27 11:19
# @Author : limber
# @desc :


from store_service.connection_pool import ConnectionPool
from store_service.model.model_script import Script
from typing import Optional, List


class ScriptMapper:
    """
    脚本代理类
    """

    def __init__(self):
        self.pool = ConnectionPool
        self.conn = self.pool.get_connection()
        self.cursor = self.conn.cursor()

    def select_by_id(self, script_id: int) -> Optional[Script]:
        """
        通过id查找脚本

        :param script_id:
        :return:
        """
        id_ = script_id
        sql_ = "select * from tb_script where id = ?;"
        params = (id_,)
        result = self.cursor.execute(sql_, params).fetchone()
        self.pool.return_connection(self.conn)

        if result is not None:
            return Script(*result)
        return result

    def select_by_app(self, app_name: str) -> List[Script]:
        """
        根据app名称查找脚本,脚本为n个

        :param app_name:
        :return:
        """

        app_name = app_name
        sql_ = "select * from tb_script where app = ?;"
        params = (app_name,)
        result = self.cursor.execute(sql_, params).fetchall()
        self.pool.return_connection(self.conn)

        if result:
            script_list_ = []
            for script_ in result:
                script_list_.append(Script(*script_))
            return script_list_
        return result

    def select_all(self) -> List[Script]:
        """
        查询全部脚本

        :return:
        """
        sql_ = "select * from tb_script"
        result = self.cursor.execute(sql_).fetchall()
        self.pool.return_connection(self.conn)
        if result:
            script_list_ = []
            for script_ in result:
                script_list_.append(Script(*script_))
            return script_list_
        return result

    def insert(self, script: Script) -> int:
        """
        插入一个脚本

        :param script:
        :return:
        """
        params = (script.script_name, script.script_content, script.app)
        sql_ = "insert into tb_script (script_name, script_content, app) values (?, ?, ?)"
        try:
            self.cursor.execute(sql_, params)
            self.conn.commit()
            return self.cursor.rowcount
        except Exception as e:
            print(str(e))
            self.conn.rollback()
        finally:
            self.pool.return_connection(self.conn)

    def delete_by_name(self, script_name) -> int:
        """
        根据脚本的名称删除脚本

        :param script_name:
        :return:
        """

        params = (script_name,)
        sql_ = "delete from tb_script where script_name = ?"
        try:
            self.cursor.execute(sql_, params)
            self.conn.commit()
            return self.cursor.rowcount
        except Exception as e:
            print(str(e))
            self.conn.rollback()
        finally:
            self.pool.return_connection(self.conn)

    def update(self, script: Script) -> int:
        """
        更新脚本

        :param script:
        :return:
        """

        params = script.to_dict()
        sql_ = (f"update tb_script set "
                f"script_name=:script_name, script_content=:script_content, app=:app "
                f"where id = {script.id}")

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
    # 添加脚本
    # script_1 = {"script_name": "prism_script_2",
    #             "script_content": "['home']",
    #             "app": "prism"}
    #
    # script_2 = {"script_name": "innova_script_1",
    #             "script_content": "['home']",
    #             "app": "innova"}
    #
    # script_3 = {"script_name": "twitter_script_1",
    #             "script_content": "['home']",
    #             "app": "twitter"}
    #
    # script_obj_1 = Script(**script_1)
    # script_obj_2 = Script(**script_2)
    # script_obj_3 = Script(**script_3)
    #
    # result = ScriptMapper().insert(script_obj_1)
    # print(result)
    # result = ScriptMapper().insert(script_obj_2)
    # print(result)
    # result = ScriptMapper().insert(script_obj_3)
    # print(result)

    # 根据name查询脚本
    # name = "twitter"
    # result = ScriptMapper().select_by_app(name)
    # for i in result:
    #     print(i)

    # 查询全部脚本
    # result = ScriptMapper().select_all()
    # for i in result:
    #     print(i)

    # 更新脚本
    # twitter_script = result[0]
    # twitter_script.app = "ins"
    # print(twitter_script)
    # result = ScriptMapper().update(twitter_script)
    # print(result)

    # 删除脚本
    # name = "twitter_script_1"
    # result = ScriptMapper().delete_by_name(name)
    # print(result)

