# -*- coding: utf-8 -*-
#@Time : 10/14/22 2:02 PM
#@Author : 知北游
#@File : token.py
#@Software : PyCharm

from models import User


def tokenVerify(token: str, user_type: str=None) -> User:
    user = User.query.filter_by(id=token).first()
    if user==None or user_type!=None and user_type != user.user_type:
        return None
    return user
