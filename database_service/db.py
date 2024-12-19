#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/18 16:15
# @Author : limber
# @desc :

from peewee import SqliteDatabase
from pathlib import Path

db_file = "database.db"
root_path = Path(__file__).parent.parent
db_file_path = root_path.joinpath("database_service").joinpath(db_file)
database = SqliteDatabase(db_file_path)
