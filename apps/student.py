# -*- coding: utf-8 -*-
# @Time : 10/9/22 3:47 PM
# @Author : 知北游
# @File : book.py
# @Software : PyCharm

from flask import Blueprint,request,jsonify,json
from models import User, Expression, Course
from exts import db
from verify import tokenVerify
import datetime

bp = Blueprint("student", __name__, url_prefix="/student")


# post到 IP/student/enter_course json包含course_code
@bp.route('/enter_course', methods=['GET'])
def student_enter_course() -> json:
    try:
        token = request.headers.get("token")
        print(token)
        user = tokenVerify(token, "student")
        if user is None:
                return jsonify({"status": "error", "data": {"info": "没有这个学生或您不是学生!"}})
        course_code = request.args.get("course_code")
        course = Course.query.filter_by(course_code=course_code).first()
        if course is not None:
            print("学生:" + user.email + "  进入课程:"+ course.course_name + "  课程Code:"+ course_code)
            db.session.commit()
            return jsonify({"status": "success", "data": {"course_id":str(course.id),
                                                          "course_name": course.course_name}})
        else:
            print(course_code)
            return jsonify({"status": "error", "data": {"info": "没有这个课程!"}})
    except (Exception) as result:
        return jsonify({"status": "error", "data": {"info": str(result)}})  # 其他错误 直接塞到json里返回


# post到IP/student/comment,其中json包含token,course_id,grade
@bp.route('/comment', methods = ['POST'])
def student_comment() -> json:
    try:
        token = request.headers.get("token")
        data = request.get_data()
        if data is None or len(data) == 0 :
            return jsonify({"status": "error", "data": {"info": "空内容"}})
        data = json.loads(data)
        course_id, grade = [data['course_id'], data['grade']]

        user = tokenVerify(token, "student")
        if user is None:
            print(data)
            return jsonify({"status": "error", "data": {"info": "没有这个学生或您不是学生!"}})
        course = Course.query.filter_by(id=course_id).first()
        if course is None:
            print(data)
            return jsonify({"status": "error", "data": {"info": "没有这个课程!"}})
        print("评价人:" + user.email + " 分数:" + grade+ " 课程:" + course.course_name)
        db.session.add(Expression(student_id=token, course_id=course_id, grade=grade, date_time = datetime.datetime.now()))
        db.session.commit()
        return jsonify({"status": "success", "data": {"course_name":course.course_name, "grade":grade}})

    except (Exception) as result:
        return jsonify({"status": "error", "data": {"info": str(result)}})  # 其他错误 直接塞到json里返回

