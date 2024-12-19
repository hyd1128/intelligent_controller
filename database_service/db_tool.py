#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/18 17:23
# @Author : limber
# @desc :


from database_service.model import (advertising_task_model,
                                    advertising_task_record_model,
                                    app_model,
                                    app_task_record_model,
                                    app_task_model,
                                    device_model,
                                    script_model)
from database_service.db import database

database.drop_tables([
    advertising_task_model.AdvertisingTask,
    advertising_task_record_model.AdvertisingTaskRecord,
    app_model.App,
    app_task_record_model.AppTaskRecord,
    app_task_model.AppTask,
    device_model.Device,
    script_model.Script
], safe=True)

database.create_tables([
    advertising_task_model.AdvertisingTask,
    advertising_task_record_model.AdvertisingTaskRecord,
    app_model.App,
    app_task_record_model.AppTaskRecord,
    app_task_model.AppTask,
    device_model.Device,
    script_model.Script
], safe=True)

