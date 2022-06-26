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

