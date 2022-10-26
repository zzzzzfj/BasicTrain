# -*- coding: utf-8 -*-
# @Time : 10/4/22 8:36 PM
# @Author : 知北游
# @File : config.py.py
# @Software : PyCharm

# character set
JSON_AS_ASCII = False

# 加密
SECRET_KEY = "adfadgaslhgaljef23286161"

# database
HOSTNAME = '172.17.0.1'  # 服务器网桥模式
if __file__ == '/Users/behaver/Developer/Python/BasicTrain/config.py':
    HOSTNAME = '127.0.0.1'  # 本地
PORT = '3306'
DATABASE = 'basictrain'
USERNAME = 'zfj'
PASSWORD = '1234'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True

# 邮箱设置
MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_DEBUG = False
MAIL_USERNAME = "2931256972@qq.com"
MAIL_PASSWORD = "yxdcuvqwlnwmdgcb"
DEFAULT_MAIL_SENDER = "2931256972@qq.com"
