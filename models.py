# -*- coding: utf-8 -*-
# @Time : 10/10/22 9:52 PM
# @Author : 知北游
# @File : models.py
# @Software : PyCharm

# 数据库的表设计
from exts import db


# from sqlalchemy.orm import scoped_session, sessionmaker

# engine = db.get_engine()
# db_session = scoped_session(sessionmaker(autocommit=True,
#                                          autoflush=False,
#                                          bind=engine))

# 学生表: id, 账号(邮箱), 密码, 学号、姓名、年龄、性别、年级、班级、专业、联系方式等基础信息
class StudentModel(db.Model):
    __tablename__ = "student"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    student_number = db.Column(db.String(200), nullable=False, unique=True)
    name = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(5))
    grade = db.Column(db.String(5))
    classroom = db.Column(db.String(5))
    major = db.Column(db.String(20))
    phone_number = db.Column(db.String(20))


# 教师表: id, 账号(邮箱), 密码, 姓名、年龄、性别、联系方式等
class TeacherModel(db.Model):
    __tablename__ = "teacher"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(5))
    phone_number = db.Column(db.String(20))


# 教师表: id, 账号(邮箱), 密码, 姓名、年龄、性别、联系方式等
class AdminModel(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(5))
    phone_number = db.Column(db.String(20))


# 登陆表:
class LoginModel(db.Model):
    __tablename__ = "login"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    user_type = db.Column(db.Enum('student', 'teacher', 'admin'), nullable=False)


# 表情表: 分数(1-6), 时间(DATE), 所属课程id
class ExpressionModel(db.Model):
    __tablename__ = "expression"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    grade = db.Column(db.Integer, nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    student_id = db.Column(db.Integer, nullable=False)
    course_id = db.Column(db.Integer, nullable=False)


# 课程表: id(课程id), 课程名称, 课程编码(classCode, 5位, 如CS201)
class CourseModel(db.Model):
    __tablename__ = "course"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_name = db.Column(db.String(200), nullable=False)
    course_code = db.Column(db.String(10), nullable=False, unique=True)


# 邮箱验证码表
class EmailCaptchaModel(db.Model):
    __tablename__ = "email_captcha"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    captcha = db.Column(db.String(10), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    user_type = db.Column(db.Enum('student', 'teacher', 'admin'), nullable=False)
