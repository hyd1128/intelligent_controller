#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/9/9 14:41
# @Author : limber
# @desc :


"""
添加一个device的全局队列工具类
"""
import queue


class DeviceQueue:
    # 为该类创建一个队列类属性
    __q = queue.Queue()

    @classmethod
    def empty(cls):
        """
        判断队列是否为空

        :return:
        """
        return cls.__q.empty()

    @classmethod
    def qsize(cls):
        """
        返回队列的大致大小

        :return:
        """
        return cls.__q.qsize()

    @classmethod
    def get(cls):
        """
        获取队列中的一个元素，没有的时候就阻塞

        :return:
        """
        return cls.__q.get(block=True)

    @classmethod
    def get_nowait(cls):
        """
        使用非阻塞的方式获取队列元素

        :return:
        """
        return cls.__q.get_nowait()

    @classmethod
    def put(cls, value):
        """
        向队列中放入一个元素

        :param value:
        :return:
        """
        cls.__q.put(value)

    @classmethod
    def join(cls):
        """
        阻塞至队列中所有的元素都被接收和处理完毕

        :return:
        """
        cls.__q.join()

    @classmethod
    def task_one(cls):
        """
        表示前面排队的任务已经被完成

        :return:
        """
        cls.__q.task_done()


if __name__ == '__main__':
    print(DeviceQueue.qsize())
    print(DeviceQueue.empty())