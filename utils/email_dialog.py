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
from PyQt5.QtWidgets import QLineEdit, QTableWidget, QTableWidgetItem, QLabel, QMessageBox

BASE_DIR = str(Path(__file__).absolute().parent.parent)


class AlertWindow(QDialog):
    def __init__(self):
        super(AlertWindow, self).__init__()
        self.field_dict = dict()
        # 窗体标题和尺寸
        self.setWindowTitle("SMTP邮件配置")
        #
        # # 窗体的尺寸
        self.resize(300, 270)

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

        path = Path(BASE_DIR) / "db" / "alert.json"
        data_dict = {}
        if path.is_file():
            data_dict = json.loads(path.read_text(encoding="utf-8"))
            print(data_dict)
            print(type(data_dict))

        form_data_list = [
            {"title": "SMTP服务器", "filed": "smtp"},
            {"title": "发件箱", "filed": "from"},
            {"title": "密码", "filed": "pwd"},
            {"title": "收件人(多个用逗号分隔)", "filed": "to"},
        ]

        for item in form_data_list:
            label = QLabel()
            label.setText(item["title"])
            layout.addWidget(label)

            txt = QLineEdit()
            filed = item["filed"]
            if data_dict and filed in data_dict.keys():
                txt.setText(data_dict[filed])
            self.field_dict[filed] = txt
            layout.addWidget(txt)

        btn_save = QPushButton("保存")
        btn_save.clicked.connect(self.event_save_click)
        layout.addWidget(btn_save, 0, Qt.AlignRight)
        self.setLayout(layout)

    def event_save_click(self):
        data_dict = {}
        for key, filed in self.field_dict.items():
            value = filed.text().strip()
            if not value:
                QMessageBox.warning(self, "错误", "邮件报警配置项不能为空")
            data_dict[key] = value
        print(data_dict)
        path = Path(BASE_DIR) / "db"
        if not path.is_dir():
            print("文件夹不存在")
            path.mkdir(parents=True, exist_ok=True)
            path = Path(path) / "alert.json"
            path.write_text(data=json.dumps(data_dict, ensure_ascii=False, indent=2), encoding="utf-8")
        else:
            print("文件夹存在")
            path = Path(path) / "alert.json"
            path.write_text(data=json.dumps(data_dict, ensure_ascii=False, indent=2), encoding="utf-8")
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = AlertWindow()
    win.show()

    sys.exit(app.exec_())
