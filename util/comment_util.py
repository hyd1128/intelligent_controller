#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2025/1/17 10:16
# @Author : limber
# @desc :
import random

import pandas as pd

from util.config_util import RESOURCES
from util.path_util import PathUtil


class CommentUtil:

    @staticmethod
    def multi_media_review(language_type: str = "EN") -> str:
        """
        读取评论列表的知识库, 每个知识库有两个语种, 语种1为english, 语种2为chinese
        可选值 EN & CN
        默认值： EN
        :param language_type:
        :return:
        """

        knowledge_path = PathUtil.get_root_path(__file__, 2).joinpath(RESOURCES).joinpath("comment_knowlege").joinpath(
            "multimedia_comment.xlsx")
        df = pd.read_excel(knowledge_path)

        # 获取总行数
        total_rows = len(df)

        # 获取随机行数
        random_row_number = random.randint(0, total_rows)

        comment_ = df.iloc[random_row_number][language_type]
        return comment_

    @staticmethod
    def place_review(language_type: str = "EN") -> str:
        knowledge_path = PathUtil.get_root_path(__file__, 2).joinpath(RESOURCES).joinpath("comment_knowlege").joinpath(
            "place_comment.xlsx")
        df = pd.read_excel(knowledge_path)

        # 获取总行数
        total_rows = len(df)

        # 获取随机行数
        random_row_number = random.randint(0, total_rows)

        comment_ = df.iloc[random_row_number][language_type]
        return comment_


if __name__ == '__main__':
    text = CommentUtil.place_review()
    print(text)
