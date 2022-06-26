#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author  : python_DJ
# @contact : 185381664@qq.com
# @Time    : 2022/6/25-23:46
# @File    : v2.py
import json
import sys
from pathlib import Path
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QWidget, QApplication, QDesktopWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtWidgets import QLineEdit, QTableWidget, QTableWidgetItem, QLabel

BASE_DIR = str(Path(__file__).absolute().parent)
# print(BASE_DIR)
STATUS_MAPPING = {
    0: "初始化中",
    1: "待执行",
    2: "正在执行",
    3: "完成并提醒",
    4: "异常并停止",
    5: "初始化失败",
}


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        # 窗体标题和尺寸
        self.setWindowTitle("亚马逊商品价格监控系统")

        # 窗体的尺寸
        self.resize(1220, 450)

        # 窗体位置
        # 当前窗口对象
        qr = self.frameGeometry()
        # 计算出当前显示器的屏幕分辨率,根据得到的分辨率，然后得到屏幕的中心点
        cp = QDesktopWidget().availableGeometry().center()
        # 然后把当前窗口的中心点移动到qr的中心点
        qr.moveCenter(cp)
        self.init_ui()

    def init_ui(self):
        # 创建垂直布局
        layout = QVBoxLayout()
        # 1.创建顶部菜单布局
        layout.addLayout(self.init_header())
        # 2.创建顶部表单布局
        layout.addLayout(self.init_form())
        # 3.创建中间表格布局
        layout.addLayout(self.init_table())
        # 4.创建底部菜单布局
        layout.addLayout(self.init_footer())
        # 设置主窗口的布局为垂直布局
        self.setLayout(layout)

    def init_header(self):
        header_layout = QHBoxLayout()
        # 创建两个按钮
        btn_start = QPushButton(text="开始")
        btn_start.setFixedSize(100, 30)
        header_layout.addWidget(btn_start)
        btn_stop = QPushButton(text="停止")
        btn_stop.setFixedSize(QSize(100, 30))
        header_layout.addWidget(btn_stop)
        header_layout.addStretch()
        return header_layout

    def init_form(self):
        form_layout = QHBoxLayout()
        txt_asin = QLineEdit()
        txt_asin.setPlaceholderText("请输入商品ID和价格，例如B2818JJQQ8=88")
        form_layout.addWidget(txt_asin)
        btn_add = QPushButton(text="添加")
        btn_add.setFixedSize(QSize(100, 30))
        form_layout.addWidget(btn_add)
        return form_layout

    def init_table(self):
        table_layout = QHBoxLayout()
        table_widget = QTableWidget(0, 8)
        table_widget.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        table_widget.horizontalHeader().setStyleSheet("QHeaderView::section{background:skyblue;color: black;}")
        # item = QTableWidgetItem()
        # item.setText("标题")
        # table_widget.setHorizontalHeaderItem(0, item)
        table_widget.setHorizontalHeaderLabels(["ASIN", "标题", "URL", "底价", "成功次数", "503次数", "状态", "频率(N秒/次)"])
        table_widget.setColumnWidth(0, 120)
        table_widget.setColumnWidth(1, 150)
        table_widget.setColumnWidth(2, 400)
        table_widget.setColumnWidth(3, 100)
        table_widget.setColumnWidth(4, 100)
        table_widget.setColumnWidth(5, 100)
        table_widget.setColumnWidth(6, 100)
        table_widget.setColumnWidth(7, 100)

        # 读取json文件
        data_list = json.loads((Path(BASE_DIR) / "db" / "db.json").read_text(encoding="utf-8"))
        current_row_count = table_widget.rowCount()
        for row_list in data_list:
            table_widget.insertRow(current_row_count)
            for r_index, row in enumerate(row_list):
                row = STATUS_MAPPING[row] if r_index == 6 else row
                cell = QTableWidgetItem(str(row))
                if r_index in [0, 4, 5, 6]:
                    # 设置单元格不可修改
                    cell.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                cell.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                table_widget.setItem(current_row_count, r_index, cell)
            current_row_count += 1

        table_layout.addWidget(table_widget)
        return table_layout

    def init_footer(self):
        footer_layout = QHBoxLayout()

        label_status = QLabel("未检测", self)
        footer_layout.addWidget(label_status)

        footer_layout.addStretch()

        btn_reinit = QPushButton(text="重新初始化")
        btn_reinit.setFixedSize(QSize(100, 30))
        footer_layout.addWidget(btn_reinit)

        btn_recheck = QPushButton(text="重新监测")
        btn_recheck.setFixedSize(QSize(100, 30))
        footer_layout.addWidget(btn_recheck)

        btn_reset_count = QPushButton(text="次数清零")
        btn_reset_count.setFixedSize(QSize(100, 30))
        footer_layout.addWidget(btn_reset_count)

        btn_delete = QPushButton(text="删除检测项")
        btn_delete.setFixedSize(QSize(100, 30))
        footer_layout.addWidget(btn_delete)

        btn_alert = QPushButton(text="SMTP报警配置")
        btn_alert.setFixedSize(QSize(100, 30))
        footer_layout.addWidget(btn_alert)

        btn_proxy = QPushButton(text="代理IP")
        btn_proxy.setFixedSize(QSize(100, 30))
        footer_layout.addWidget(btn_proxy)
        return footer_layout


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = MainWindow()
    win.show()

    sys.exit(app.exec_())
