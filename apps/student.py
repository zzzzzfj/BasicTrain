# -*- coding: utf-8 -*-
# @Time : 10/9/22 3:47 PM
# @Author : 知北游
# @File : book.py
# @Software : PyCharm

from flask import Blueprint, request, jsonify, json, g
from models import CourseModel, ExpressionModel
from exts import db
import datetime

bp = Blueprint("student", __name__, url_prefix="/student")


# post到 IP/student/enter_course json包含course_code
@bp.route('/enter_course', methods=['GET'])
def student_enter_course() -> json:
    try:
        course_code = request.args.get("course_code")
        course = CourseModel.query.filter_by(course_code=course_code).first()
        if course:
            print("学生:" + str(g.user_id) + "  进入课程:" + course.course_name + "  课程Code:" + course_code)
            return jsonify({"status": "success", "data": {"course_id": str(course.id),
                                                          "course_name": course.course_name}})
        else:
            return jsonify({"status": "error", "data": {"info": "没有这个课程!"}})
    except Exception as result:
        return jsonify({"status": "error", "data": {"info": str(result)}})


# post到IP/student/comment,其中json包含token,course_id,grade
@bp.route('/comment', methods=['POST'])
def student_comment() -> json:
    if g.user_type != 'student':
        return jsonify({"status": "error", "data": {"info": "您不是学生, 无法评价!"}})
    try:
        data = request.get_data()
        data = json.loads(data)
        course_id, grade = [data['course_id'], data['grade']]
        course = CourseModel.query.filter_by(id=course_id).first()
        if course:
            print("评价人:学生" + str(g.user_id) + " 分数:" + grade + " 课程:" + course.course_name)
            db.session.add(ExpressionModel(student_id=g.user_id,
                                           course_id=course_id,
                                           grade=grade,
                                           date_time=datetime.datetime.utcnow() + datetime.timedelta(hours=8)))
            db.session.commit()
            return jsonify({"status": "success", "data": {"course_name": course.course_name, "grade": grade}})
        else:
            return jsonify({"status": "error", "data": {"info": "没有这个课程!"}})
    except Exception as result:
        return jsonify({"status": "error", "data": {"info": str(result)}})
