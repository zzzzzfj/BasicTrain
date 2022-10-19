# -*- coding: utf-8 -*-
#@Time : 10/10/22 9:52 PM
#@Author : 知北游
#@File : models.py
#@Software : PyCharm

# 数据库的表设计
from exts import db
from sqlalchemy.orm import scoped_session, sessionmaker

# engine = db.get_engine()
# db_session = scoped_session(sessionmaker(autocommit=True,
#                                          autoflush=False,
#                                          bind=engine))

# 账号表: id, 账号(邮箱), 密码, 用户类型(student,teacher,admin)
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    user_type = db.Column(db.Enum('student','teacher','admin'), nullable=False)

# 登陆表: pass

# 表情表: 分数(1-6), 时间(DATE), 所属课程id
class Expression(db.Model):
    __tablename__ = "expression"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    grade = db.Column(db.Integer, nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    student_id = db.Column(db.Integer, nullable=False)
    course_id = db.Column(db.Integer, nullable=False)

# 课程表: id(课程id), 课程名称, 课程编码(classCode, 5位, 如CS201)
class Course(db.Model):
    __tablename__ = "course"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_name = db.Column(db.String(200), nullable=False)
    course_code = db.Column(db.String(10), nullable=False)




