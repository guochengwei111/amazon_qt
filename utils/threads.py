#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author  : python_DJ
# @contact : 185381664@qq.com
# @Time    : 2022/6/26-15:45
# @File    : threads.py
import time

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
