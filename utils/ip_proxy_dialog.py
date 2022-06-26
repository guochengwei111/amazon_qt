#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author  : python_DJ
# @contact : 185381664@qq.com
# @Time    : 2022/6/26-17:10
# @File    : email_dialog.py
import json
import sys
from pathlib import Path
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QWidget, QApplication, QDesktopWidget, QVBoxLayout, QHBoxLayout, QPushButton, QDialog
from PyQt5.QtWidgets import QLineEdit, QTableWidget, QTableWidgetItem, QLabel, QMessageBox, QTextEdit

BASE_DIR = str(Path(__file__).absolute().parent.parent)


class ProxyWindow(QDialog):
    def __init__(self):
        super(ProxyWindow, self).__init__()
        self.txt = None
        # 窗体标题和尺寸
        self.setWindowTitle("ip代理配置")
        #
        # # 窗体的尺寸
        self.resize(500, 400)

        # 窗体位置
        # # 当前窗口对象
        # qr = self.frameGeometry()
        # # 计算出当前显示器的屏幕分辨率,根据得到的分辨率，然后得到屏幕的中心点
        # cp = QDesktopWidget().availableGeometry().center()
        # # 然后把当前窗口的中心点移动到qr的中心点
        # qr.moveCenter(cp)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        path = Path(BASE_DIR) / "db" / "proxy.txt"
        data_str = ""
        if path.is_file():
            data_str = path.read_text(encoding="utf-8")
            print(data_str)
            print(type(data_str))

        txt = QTextEdit()
        txt.setText(data_str)
        self.txt = txt
        layout.addWidget(txt)

        btn_reset = QPushButton("重置")
        btn_reset.clicked.connect(self.event_reset_click)
        layout.addWidget(btn_reset, 0, Qt.AlignRight)
        self.setLayout(layout)

    def event_reset_click(self):
        "重置ip"
        data_str = self.txt.toPlainText()
        print(data_str)
        path = Path(BASE_DIR) / "db"
        if not path.is_dir():
            print("文件夹不存在")
            path.mkdir(parents=True, exist_ok=True)
            path = Path(path) / "proxy.txt"
            path.write_text(data=data_str, encoding="utf-8")
        else:
            print("文件夹存在")
            path = Path(path) / "proxy.txt"
            path.write_text(data=data_str, encoding="utf-8")
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = ProxyWindow()
    win.show()

    sys.exit(app.exec_())
