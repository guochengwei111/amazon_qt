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
from PyQt5.QtWidgets import QWidget, QApplication, QDesktopWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMenu
from PyQt5.QtWidgets import QLineEdit, QTableWidget, QTableWidgetItem, QLabel, QMessageBox
from utils.threads import NewTaskThread
from utils.email_dialog import AlertWindow
from utils.ip_proxy_dialog import ProxyWindow
from utils.log_dialog import LogWindow
from utils.scheduler import Scheduler

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
        self.txt_asin = None
        self.table_widget = None
        self.label_status = None
        self.scheduler = Scheduler()
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
        self.new_task_thread = NewTaskThread()
        self.new_task_thread.success.connect(self.init_task_success_slot)
        self.new_task_thread.error.connect(self.init_task_error_slot)

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
        btn_start.clicked.connect(self.event_start_click)
        header_layout.addWidget(btn_start)
        btn_stop = QPushButton(text="停止")
        btn_stop.setFixedSize(QSize(100, 30))
        btn_stop.clicked.connect(self.event_stop_click)
        header_layout.addWidget(btn_stop)
        header_layout.addStretch()
        return header_layout

    def init_form(self):
        form_layout = QHBoxLayout()
        txt_asin = QLineEdit()
        txt_asin.setPlaceholderText("请输入商品ID和价格，例如B2818JJQQ8=88")
        self.txt_asin = txt_asin
        txt_asin.setText("e123=10")
        form_layout.addWidget(txt_asin)
        btn_add = QPushButton(text="添加")
        btn_add.clicked.connect(self.event_add_click)
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
        self.table_widget = table_widget

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

        # 设置table表格可以右键配置菜单
        table_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        table_widget.customContextMenuRequested.connect(self.table_reght_menu)

        table_layout.addWidget(table_widget)
        return table_layout

    def init_footer(self):
        footer_layout = QHBoxLayout()

        label_status = QLabel("未检测", self)
        self.label_status = label_status
        footer_layout.addWidget(label_status)

        footer_layout.addStretch()

        btn_reinit = QPushButton(text="重新初始化")
        btn_reinit.setFixedSize(QSize(100, 30))
        btn_reinit.clicked.connect(self.event_reset_click)
        footer_layout.addWidget(btn_reinit)

        btn_recheck = QPushButton(text="重新监测")
        btn_recheck.setFixedSize(QSize(100, 30))
        footer_layout.addWidget(btn_recheck)

        btn_reset_count = QPushButton(text="次数清零")
        btn_reset_count.setFixedSize(QSize(100, 30))
        btn_reset_count.clicked.connect(self.event_reset_count_click)
        footer_layout.addWidget(btn_reset_count)

        btn_delete = QPushButton(text="删除检测项")
        btn_delete.setFixedSize(QSize(100, 30))
        btn_delete.clicked.connect(self.event_delete_click)
        footer_layout.addWidget(btn_delete)

        btn_alert = QPushButton(text="SMTP报警配置")
        btn_alert.setFixedSize(QSize(100, 30))
        btn_alert.clicked.connect(self.event_alert_click)
        footer_layout.addWidget(btn_alert)

        btn_proxy = QPushButton(text="代理IP")
        btn_proxy.setFixedSize(QSize(100, 30))
        btn_proxy.clicked.connect(self.event_proxy_click)
        footer_layout.addWidget(btn_proxy)
        return footer_layout

    def event_add_click(self):
        """
        点击添加按钮
        :return:
        """
        # 获取数据
        text = str(self.txt_asin.text()).strip()
        print(text)
        if not text:
            mes = QMessageBox(QMessageBox.Warning, "错误", "输入错误")
            mesY = mes.addButton(self.tr("确定"), QMessageBox.YesRole)
            mesN = mes.addButton(self.tr("取消"), QMessageBox.NoRole)
            mes.exec_()
            if mes.clickedButton() == mesY:
                print("您点击了yes")
            elif mes.clickedButton() == mesN:
                return
        asin, price = text.split("=")
        price = float(price)
        # 构造初始数据
        new_row_list = [asin, "", "", price, 0, 0, 0, 5]
        current_row_count = self.table_widget.rowCount()
        self.table_widget.insertRow(current_row_count)
        for r_index, row in enumerate(new_row_list):
            row = STATUS_MAPPING[row] if r_index == 6 else row
            cell = QTableWidgetItem(str(row))
            if r_index in [0, 4, 5, 6]:
                # 设置单元格不可修改
                cell.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            cell.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.table_widget.setItem(current_row_count, r_index, cell)
        # 发送请求，获取标题和url，需要在线程中处理这个任务
        self.new_task_thread.row_index = current_row_count
        self.new_task_thread.asin = asin
        self.new_task_thread.start()

    def init_task_success_slot(self, rol_index, asin, title, url):
        print(rol_index, asin, title, url)
        # 更新标题
        cell_title = QTableWidgetItem()
        cell_title.setText(title)
        cell_title.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.table_widget.setItem(rol_index, 1, cell_title)
        # 更新url
        cell_url = QTableWidgetItem()
        cell_url.setText(url)
        cell_url.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.table_widget.setItem(rol_index, 2, cell_url)
        # 更新状态
        cell_status = QTableWidgetItem()
        cell_status.setText(STATUS_MAPPING[1])
        cell_status.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        cell_status.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.table_widget.setItem(rol_index, 6, cell_status)

        # 清空输入框
        self.txt_asin.clear()

    def init_task_error_slot(self, rol_index, asin, title, url):
        print(rol_index, asin, title, url)

    def event_reset_click(self):
        # 获取所选中得行
        row_list = self.table_widget.selectionModel().selectedRows()
        print(row_list)
        if not row_list:
            QMessageBox.warning(self, "错误", "请选择要重新初始化的行")
        # 获取每一行
        for row in row_list:
            row_index = row.row()
            asin = self.table_widget.item(row_index, 0).text().strip()  # 获取表格某一行的第0列
            print("选中的行：{}".format(row_index))
            # 更新状态
            cell_status = QTableWidgetItem()
            cell_status.setText(STATUS_MAPPING[0])
            cell_status.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            cell_status.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.table_widget.setItem(row_index, 6, cell_status)
            # 创建线程
            self.new_task_thread.row_index = row_index
            self.new_task_thread.asin = asin
            self.new_task_thread.start()

    def event_reset_count_click(self):
        """
        次数清零
        :return:
        """
        # 获取所选中得行
        row_list = self.table_widget.selectionModel().selectedRows()
        print(row_list)
        if not row_list:
            QMessageBox.warning(self, "错误", "请选择要重新初始化的行")
        # 获取每一行
        for row in row_list:
            row_index = row.row()
            print("选中的行：{}".format(row_index))
            # 更新次数归零
            cell_4 = QTableWidgetItem()
            cell_4.setText(str(0))
            cell_4.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            cell_4.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.table_widget.setItem(row_index, 4, cell_4)

            cell_5 = QTableWidgetItem()
            cell_5.setText(str(0))
            cell_5.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            cell_5.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.table_widget.setItem(row_index, 5, cell_5)

    def event_delete_click(self):
        row_list = self.table_widget.selectionModel().selectedRows()
        row_list.reverse()  # 删除前列表翻转
        print(row_list)
        if not row_list:
            QMessageBox.warning(self, "错误", "请选择要重新初始化的行")
        # 获取每一行
        for row in row_list:
            row_index = row.row()
            self.table_widget.removeRow(row_index)

    def event_alert_click(self):
        """
        邮件配置
        :return:
        """
        dialog = AlertWindow()
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.exec_()

    def event_proxy_click(self):
        """
        ip配置
        :return:
        """
        dialog = ProxyWindow()
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.exec_()

    def table_reght_menu(self, pos):
        # 只选中一行时，才支持右键
        selected_item_list = self.table_widget.selectedItems()

        if len(selected_item_list) == 0:
            return
        if len(selected_item_list) > 1:
            return
        menu = QMenu()
        item_copy = menu.addAction("复制")
        item_log = menu.addAction("查看日志")
        item_log_clear = menu.addAction("清除日志")

        # action就是选中了哪个菜单
        action = menu.exec_(self.table_widget.mapToGlobal(pos))
        if action == item_copy:
            clipboard = QApplication.clipboard()
            # clipboard.setText(selected_item_list[0].text())
            # 获取当前单元格里面的数据
            clipboard.setText(self.table_widget.currentIndex().data())
        if action == item_log:
            row_index = selected_item_list[0].row()  # 当前行索引
            asin = self.table_widget.item(row_index, 0).text().strip()  # 获取某行第一列的单元格数据
            dialog = LogWindow(asin=asin)
            dialog.setWindowModality(Qt.ApplicationModal)
            dialog.exec_()
        if action == item_log_clear:
            row_index = selected_item_list[0].row()  # 当前行索引
            asin = self.table_widget.item(row_index, 0).text().strip()  # 获取某行第一列的单元格数据
            path = Path(BASE_DIR) / "log" / "{}.log".format(asin)
            if path.exists():
                path.unlink()
                QMessageBox.information(self, "正常", "文件已删除", QMessageBox.Yes)

    def event_start_click(self):
        """
        开始按钮
        :return:
        """
        # 为每一行创建一个线程（记录创建的所有线程）
        # self是当前的窗口对象，回调函数有调度器的信号connect触发
        self.scheduler.start(
            self,
            BASE_DIR,
            self.task_start_callback,
            self.task_counter_callback,
            self.task_stop_callback,
        )

        # 状态显示执行中 【线程个数为0，修改状态】
        self.update_status_message("执行中")

    def task_start_callback(self, row_index):
        """
        开始按钮的回调函数
        对表格中的数据进行状态的更新
        :return:
        """
        cell_status = QTableWidgetItem()
        cell_status.setText(STATUS_MAPPING[2])
        cell_status.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        cell_status.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.table_widget.setItem(row_index, 6, cell_status)

    def task_counter_callback(self, row_index, bool_value):
        """
        成功或失败，次数的加减
        :param row_index:
        :return:
        """
        # 获取原次数
        count_num = int(self.table_widget.item(row_index, 4).text().strip())
        if bool_value:
            count_num += 1
        else:
            count_num -= 1
        if count_num < 0:
            count_num = 0
        cell_status = QTableWidgetItem()
        cell_status.setText(str(count_num))
        cell_status.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        cell_status.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.table_widget.setItem(row_index, 4, cell_status)

    def task_stop_callback(self, row_index):
        """
        停止后修改当前行的执行状态
        :param row_index:当前行索引
        :return:
        """
        cell_status = QTableWidgetItem()
        cell_status.setText(STATUS_MAPPING[1])
        cell_status.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        cell_status.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.table_widget.setItem(row_index, 6, cell_status)

    def event_stop_click(self):
        """
        停止按钮
        :return:
        """
        # 逐一停止每一个线程

        # self.scheduler.stop(self.update_status_message)
        # 状态显示执行中 【线程个数为0，修改状态】
        self.update_status_message("未检测")

    def update_status_message(self, message):
        self.label_status.setText(message)
        self.label_status.repaint()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = MainWindow()
    win.show()

    sys.exit(app.exec_())
