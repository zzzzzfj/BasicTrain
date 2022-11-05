# -*- coding: utf-8 -*-
# @Time : 11/5/22 3:24 PM
# @Author : ZhuFujun
# @File : chatroom.py
# @Software : PyCharm

from flask import request
from exts import socketio
from flask_socketio import emit, join_room, leave_room
from models import LoginModel, StudentModel, TeacherModel, AdminModel


@socketio.on('connect')
def connect():
    print("连接建立")
    print(request)
    token = request.headers.get("token")
    login_row = LoginModel.query.filter_by(token=token).first()
    if login_row:
        if login_row.user_type == "student":
            user_row = StudentModel.query.filter_by(id=login_row.user_id).first()
        elif login_row.user_type == "teacher":
            user_row = TeacherModel.query.filter_by(id=login_row.user_id).first()
        elif login_row\
                .user_type == "admin":
            user_row = AdminModel.query.filter_by(id=login_row.user_id).first()
        if user_row:
            emit('connected', {'status': 'success',
                               'user_name': user_row.name
                               })
            return None
    emit('connected', {'status': 'error'})


@socketio.on('disconnect')
def disconnect():
    print('您已离线')
    emit('message', {'data': '连接断开',
                     'user': 'system'
                     })


# 发送给聊天室内所有人
@socketio.on('send_message')
def send_message(message):
    print(message)
    emit('message', {'data': message['data'],
                     'user_name': message['user_name']
                     }, to=message['room'])


# 进入房间
@socketio.event
def joinRoom(message):
    join_room(message['room'])
    print("join room: ", message)

    emit("roomJoined", {
        "room": message['room'],
        'user_name': message['user_name']
    }, to=message['room'])


# 退出房间
@socketio.event
def leaveRoom(message):
    emit("roomLeftPersonal", {'room': message['room'],
                              'user_name': message['user_name']
                              })
    leave_room(message['room'])
    emit("roomLeft", {
        'user_name': message['user_name'],
        "room": message['room']
    }, to=message['room'])
