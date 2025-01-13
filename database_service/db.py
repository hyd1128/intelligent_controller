#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/18 16:15
# @Author : limber
# @desc :

from peewee import SqliteDatabase

from util.config_util import RESOURCES
from util.path_util import PathUtil

db_file = "database.db"
root_path = PathUtil.get_root_path(__file__, 2)
db_file_path = root_path.joinpath(RESOURCES).joinpath("database").joinpath(db_file)
database = SqliteDatabase(db_file_path)
