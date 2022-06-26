#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author  : python_DJ
# @contact : 185381664@qq.com
# @Time    : 2022/6/26-21:56
# @File    : scheduler.py

class Scheduler:
    """
    单例模式线程调度器
    """

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Scheduler, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.thread_list = []

    def start(self):
        # 获取表格中的所有数据，每一行创建一个宪哥线程去执行
        # 每个线程成功/失败的状态，实时显示到表格中，信号+槽
        pass

    def stop(self):
        pass


if __name__ == '__main__':
    s = Scheduler()
