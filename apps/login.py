# -*- coding: utf-8 -*-
# @Time : 10/25/22 2:56 PM
# @Author : ZhuFujun
# @File : login.py
# @Software : PyCharm

from flask import Blueprint, jsonify, json, request
from werkzeug.security import generate_password_hash
from flask_mail import Message
from exts import db, mail
from models import StudentModel, TeacherModel, AdminModel, LoginModel, EmailCaptchaModel
import datetime, string, random

bp = Blueprint("login", __name__, url_prefix="/login")


# request包含 email, password, user_type 三项
@bp.route('/', methods=['GET', 'POST'])
def login() -> json:
    if request.method == "GET":
        return render_template("login.html")
    else:
        try:
            data = request.get_data()
            data = json.loads(data)
            print("登陆尝试: ", request.remote_addr, "\n用户数据", data)
            email = data['email']
            password = data['password']
            user_type = data['user_type']
            if user_type == "student":
                user = StudentModel.query.filter_by(email=email,
                                                    password=password).first()
            elif user_type == "teacher":
                user = TeacherModel.query.filter_by(email=email,
                                                    password=password).first()
            elif user_type == "admin":
                user = AdminModel.query.filter_by(email=email,
                                                  password=password).first()
            if user:
                token = new_login(user_id=user.id, user_type=user_type)
                return jsonify({"status": "success", "data": {"token": token}})
            else:
                return jsonify({"status": "error", "data": {"info": "账号或密码错误"}})
        except Exception as result:
            return jsonify({"status": "error", "data": {"info": str(result)}})  # 其他错误 直接塞到json里返回


# request包含 email, user_type 两项
@bp.route("/send_email_captcha", methods=["POST"])
def send_email_captcha() -> json:
    try:
        data = request.get_data()
        data = json.loads(data)
        email = data["email"]
        user_type = data["user_type"]
        if user_type == "student":
            user = StudentModel.query.filter_by(email=email).first()
        elif user_type == "teacher":
            user = TeacherModel.query.filter_by(email=email).first()
        elif user_type == "admin":
            user = AdminModel.query.filter_by(email=email).first()
        if user:
            my_letters = string.ascii_letters + string.digits
            captcha = "".join(random.sample(my_letters, 4))
            print(email, "获取验证码:", captcha)
            message = Message(
                subject="【BasicTrainProject】邮箱验证码登陆",
                recipients=[email],
                body="您的登陆验证码为:\n" + captcha + "\n120秒后过期,请尽快使用",
                sender="2931256972@qq.com"
            )
            mail.send(message)
            row_captcha = EmailCaptchaModel.query.filter_by(email=email).first()
            cur_time = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
            if row_captcha:
                row_captcha.captcha = captcha
                row_captcha.create_time = cur_time
                db.session.commit()
            else:
                db.session.add(EmailCaptchaModel(email=email,
                                                 captcha=captcha,
                                                 create_time=cur_time,
                                                 user_id=user.id,
                                                 user_type=user_type))
                db.session.commit()
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "error", "data": {"info": "账号错误!"}})
    except Exception as result:
        return jsonify({"status": "error", "data": {"info": str(result)}})


# request包含 email, captcha 两项
@bp.route('/verify_email_captcha', methods=['POST'])
def verify_email_captcha() -> json:
    try:
        data = request.get_data()
        data = json.loads(data)
        email = data['email']
        captcha = data['captcha']
        row_captcha = EmailCaptchaModel.query.filter_by(email=email,
                                                        captcha=captcha).first()
        cur_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).timestamp()
        if row_captcha and cur_time-row_captcha.create_time.timestamp() < 120:  # 有且未过期(120s)
            print(cur_time-row_captcha.create_time.timestamp())
            token = new_login(user_id=row_captcha.user_id, user_type=row_captcha.user_type)
            return jsonify({"status": "success", "data": {"token": token}})
        else:
            return jsonify({"status": "error", "data": {"info": "验证码错误!"}})
    except Exception as result:
        return jsonify({"status": "error", "data": {"info": str(result)}})


def new_login(user_id: int, user_type: str) -> str:
    token = generate_password_hash(str(user_id) + user_type + str(datetime.datetime.utcnow()))
    cur_user = LoginModel.query.filter_by(user_type=user_type,
                                          user_id=user_id).first()
    if cur_user:
        cur_user.token = token
        db.session.commit()
    else:
        db.session.add(LoginModel(token=token,
                                  user_id=user_id,
                                  user_type=user_type))
        db.session.commit()
    return token
