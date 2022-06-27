#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author  : python_DJ
# @contact : 185381664@qq.com
# @Time    : 2022/6/26-15:45
# @File    : threads.py
import time
from pathlib import Path
from random import randint
from PyQt5.QtCore import QThread, pyqtSignal


class NewTaskThread(QThread):
    success = pyqtSignal(int, str, str, str)
    error = pyqtSignal(int, str, str, str)

    def __init__(self, *args, **kwargs):
        super(NewTaskThread, self).__init__(*args, **kwargs)
        self.row_index = None
        self.asin = None

    def run(self) -> None:
        """线程任务"""
        time.sleep(3)
        self.success.emit(self.row_index, self.asin, "标题", "url")


class TaskThread(QThread):
    start_signal = pyqtSignal(int)
    stop_signal = pyqtSignal(int)
    count_signal = pyqtSignal(int, bool)

    def __init__(self, *args, **kwargs):
        super(TaskThread, self).__init__(*args, **kwargs)
        self.scheduler = None
        self.row_index = None
        self.asin = None
        self.log_file_path = None

    def run(self) -> None:
        """线程任务"""
        time.sleep(3)
        self.start_signal.emit(self.row_index)
        while True:
            # scheduler 对象里面有一个terminate属性，更具它的值来判断是否结束线程
            if self.scheduler.terminate:
                # 如果点击停止，则停止线程,并且修改当前行的状态
                self.stop_signal.emit(self.row_index)
                # self就是指当前的线程对象，调用scheduler对象里面的方法，列表移除对象本身，并return结束
                self.scheduler.destroy_thread(self)
                return
            time.sleep(randint(2, 5))
            if not Path(self.log_file_path).exists():
                print("日志文件不存在{}".format(self.asin))
                Path(self.log_file_path).mkdir(parents=True, exist_ok=True)
                path = Path(self.log_file_path) / "{}.log".format(self.asin)
                with open(str(path),"a",encoding="utf-8") as f:
                    f.write(str(self.row_index)+"\n")
            else:
                print("日志文件存在{}".format(self.asin))
                path = Path(self.log_file_path) / "{}.log".format(self.asin)
                with open(str(path),"a",encoding="utf-8") as f:
                    f.write(str(self.row_index)+"\n")
            self.count_signal.emit(self.row_index, True)


class StopThread(QThread):
    """
    停止按钮，监控线程列表的个数
    """
    update_signal = pyqtSignal(str)

    def __init__(self):
        super(StopThread, self).__init__()
        self.scheduler = None

    def run(self) -> None:
        # 监测线程的数量
        total_count = len(self.scheduler.thread_list)  # 总线程数量
        while True:
            running_count = len(self.scheduler.thread_list)  # 剩余线程数量
            # 更新页面
            self.update_signal.emit("正在终止，存活线程：{}/{}".format(running_count, total_count))
            if running_count == 0:
                self.update_signal.emit("已终止")
                break
            time.sleep(1)
        pass
