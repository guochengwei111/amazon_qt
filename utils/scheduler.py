#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author  : python_DJ
# @contact : 185381664@qq.com
# @Time    : 2022/6/26-21:56
# @File    : scheduler.py
from pathlib import Path

from utils.threads import TaskThread
from utils.threads import StopThread


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
        self.window = None
        self.terminate = False  # 点击停止

    def start(self, window, base_dir, fn_start, fn_count, fn_stop):
        self.window = window
        self.terminate = False
        # 获取表格中的所有数据，每一行创建一个宪哥线程去执行
        for row_index in range(window.table_widget.rowCount()):
            # row_index 每一行数据
            asin = window.table_widget.item(row_index, 0).text().strip()
            url = window.table_widget.item(row_index, 2).text().strip()
            status_text = window.table_widget.item(row_index, 6).text().strip()
            log_file_path = Path(base_dir) / "log"
            # 只有是待执行时，才创建线程
            if status_text != "待执行":
                continue
            # 每个线程成功/失败的状态，实时显示到表格中，信号+槽
            t = TaskThread()
            t.scheduler = self
            t.row_index = row_index
            t.asin = asin
            t.log_file_path = log_file_path
            t.start_signal.connect(fn_start)
            t.count_signal.connect(fn_count)
            t.stop_signal.connect(fn_stop)  # 信号连接到回调函数
            t.start()
            self.thread_list.append(t)  # 每一个线程对象都添加到列表
        pass

    def stop(self,fn_stop):
        self.terminate = True
        # 新创建一个线程 监测 thread_list中数量并实时更新窗体label
        t = StopThread()
        t.scheduler = self
        # t.update_signal.connect(self.window.update_status_message)
        t.update_signal.connect(fn_stop)
        t.start()

    def destroy_thread(self, thread):
        """
        移除线程列表里面的线程对象
        :param thread:
        :return:
        """
        self.thread_list.remove(thread)


if __name__ == '__main__':
    s = Scheduler()
