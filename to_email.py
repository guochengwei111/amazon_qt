#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author  : python_DJ
# @contact : 185381664@qq.com
# @Time    : 2022/6/26-16:52
# @File    : to_email.py

# 1.将python内置的模块(功能导入)

import smtplib
from datetime import datetime
from smtplib import SMTP_SSL
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from email.mime.text import MIMEText
from email.utils import formataddr


class EmailHandler(object):

    def __init__(self):
        """
         :param user:str 发送人邮箱地址（用户名）
         :param password:str 发送人在QQ或163申请的授权码
         :param type:int 0 为QQ邮箱 1 为163邮箱
         """
        self.host_server = 'smtp.qq.com'  # qq邮箱smtp服务器
        self.sender_qq = '185381664@qq.com'  # 发件人邮箱
        self.pwd = 'xbgioqfzuairbhie'
        self.receiver1 = 'gcw-410@qq.com'
        self.receiver2 = 'guochengwei@guanwen100.com'
        self.mail_title = '运行异常，紧急排查'  # 邮件标题

    def send_email(self, info):
        # 邮件正文内容
        mail_content = "<h3>我》{}《</h3><p>运行异常，{}：{}</p>".format("骄傲了", info, datetime.now())

        msg = MIMEMultipart()
        msg["Subject"] = Header(self.mail_title, 'utf-8')
        msg["From"] = self.sender_qq
        msg["To"] = Header("插件预警邮箱", "utf-8")
        msg.attach(MIMEText(mail_content, 'html'))

        try:
            smtp = SMTP_SSL(self.host_server)  # ssl登录连接到邮件服务器
            # smtp.set_debuglevel(1)  # 0是关闭，1是开启debug
            # smtp.starttls()  # 开启安全传输模式
            smtp.ehlo(self.host_server)  # 跟服务器打招呼，告诉它我们准备连接，最好加上这行代码
            smtp.login(self.sender_qq, self.pwd)
            smtp.sendmail(self.sender_qq, [self.receiver1], msg.as_string())
            smtp.quit()
            smtp.close()
            print("邮件发送成功")
        except smtplib.SMTPException:
            print("无法发送邮件")


if __name__ == '__main__':
    eh = EmailHandler()
    eh.send_email("hello world!")
