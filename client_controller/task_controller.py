#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/11/26 7:43
# @Author : limber
# @desc :
import json
import os.path
import zipfile
from datetime import datetime
from io import BytesIO

import requests

from util.http_util import HttpUtils
from util.path_util import PathUtil
from util.file_util import FileUtil
from store_service.model.model_script import Script
from store_service.model.model_task import Task
from store_service.service.service_script import ScriptService
from store_service.service.service_task import TaskService


class TaskController:
    @staticmethod
    def pull_task():
        latest_task = TaskService().select_all_no_condition()[-1]
        latest_task_release_date = datetime.strptime(latest_task.task_release_date, "%Y-%m-%d")
        today_ = datetime.now()
        duration_timedelta = today_ - latest_task_release_date
        if duration_timedelta.days <= 1:
            return {
                "result": False,
                "msg": "当前任务已为最新"
            }

        URI = "/api/v1/root_accounts/task/download_tasks"
        today_ = datetime.now().strftime("%Y-%m-%d")
        json_data = {"part_task_id": today_}
        response_data = HttpUtils.post(uri=URI, json_data=json_data)
        if response_data["code"] == 200 and response_data["data"]["code"] == 200:
            if not response_data["data"]["data"]:
                return {
                    "result": False,
                    "msg": "今日无任务发布"
                }

            ####################### 下载 template ##########################
            for task_ in response_data["data"]["data"]:
                current_task_script_template_url = task_["task_url"]
                response_content = requests.get(current_task_script_template_url)

                root_path = PathUtil.get_current_file_absolute_path(__file__).parent.parent
                store_template_path = root_path.joinpath("app").joinpath("script_template")
                current_task_store_template_folder_name = task_["uuid"]
                current_task_store_template_path = store_template_path.joinpath(current_task_store_template_folder_name)
                if not current_task_store_template_path.exists():
                    current_task_store_template_path.mkdir(exist_ok=True)
                with zipfile.ZipFile(BytesIO(response_content.content)) as zip_file:
                    # 解压时忽略顶层文件夹
                    for member in zip_file.namelist():
                        member_path = member.split('/', 1)[-1]  # 去掉顶层文件夹部分
                        if member_path:  # 跳过空路径
                            target_path = os.path.join(current_task_store_template_path, member_path)
                            if member.endswith('/'):
                                continue
                            else:
                                with zip_file.open(member) as source, open(target_path, 'wb') as target:
                                    target.write(source.read())
                ################################################################

                # 获取任务和脚本内容
                current_task_content = json.loads(task_["task_content"])
                # 当前任务的任务内容
                current_task_detail_content = current_task_content["task"]
                # 当前任务的脚本内容
                current_task_script = current_task_content["script"]
                # 当前任务的脚本的脚本内容
                current_task_script_content = current_task_script["script_content"]
                for i in range(len(current_task_script_content)):
                    if (".png" in current_task_script_content[i]) or (".jpg" in current_task_script_content[i]):
                        current_task_script_content[i] = os.path.join(current_task_store_template_path,
                                                                      current_task_script_content[i])

                # 持久化一条脚本到本地数据库
                _script_ = Script(script_name=task_["uuid"] + "_script",
                                  script_content=str(current_task_script_content),
                                  app=current_task_script["app"])
                ScriptService().insert_script(_script_)

                # 持久化一条任务到本地数据库
                _task_detail = Task(task_name=current_task_detail_content["task_name"],
                                    task_execution_duration=current_task_detail_content["task_execution_duration"],
                                    min_execution_times=current_task_detail_content["min_execution_times"],
                                    max_execution_times=current_task_detail_content["max_executions_times"],
                                    task_release_date=current_task_detail_content["task_release_date"],
                                    app=current_task_detail_content["app"])
                TaskService().add_task(_task_detail)
            return {
                "result": True,
                "msg": "今日任务已全部更新"
            }
        return {
            "result": False,
            "msg": "请稍后尝试更新任务"
        }


if __name__ == '__main__':
    TaskController.pull_task()
    # str_ = "prism/"
    # str_list = str_.split("/", 1)
    # print(str_list)
