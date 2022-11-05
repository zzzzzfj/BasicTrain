# -*- coding: utf-8 -*-
# @Time : 10/10/22 9:56 PM
# @Author : 知北游
# @File : exts.py
# @Software : PyCharm


# 数据库绑定中介
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_socketio import SocketIO

db = SQLAlchemy()
mail = Mail()
socketio = SocketIO()

