# -*- coding: utf-8 -*-
# @Time : 10/10/22 11:17 PM
# @Author : 知北游
# @File : teacher.py
# @Software : PyCharm

from flask import Blueprint, request, jsonify, json, send_file, g
from models import CourseModel
from exts import db
import xlwt  # excel操作

bp = Blueprint("teacher", __name__, url_prefix="/teacher")


# post到 IP/teacher/enter_course json包含token,course_code
@bp.route('/enter_course', methods=['GET'])
def teacher_enter_course() -> json:
    try:
        course_code = request.args.get("course_code")
        course = CourseModel.query.filter_by(course_code=course_code).first()
        if course:
            print("老师:" + str(g.user_id) + "  进入课程:" + course.course_name + "  课程Code:" + course_code)
            return jsonify({"status": "success", "data": {"course_id": str(course.id),
                                                          "course_name": course.course_name}})
        else:
            return jsonify({"status": "error", "data": {"info": "没有这个课程!"}})
    except Exception as result:
        return jsonify({"status": "error", "data": {"info": str(result)}})


# 参数: datetime_start, datetime_end, course_id, return_type = "json" / "excel"
@bp.route('/query', methods=['GET'])
def teacher_query() -> json:
    try:
        # 从查询字符串得到数据
        datetime_start = request.args.get("datetime_start")
        datetime_end = request.args.get("datetime_end")
        course_id = request.args.get("course_id")
        return_type = request.args.get("return_type")
        if not datetime_start or not datetime_end or not course_id or not return_type:
            return jsonify({"status": "error", "data": {"info": "参数空缺!"}})
        response_data = {}
        # 计算 student_num, expression_num, average_grade, variance
        sql1 = '''
            SELECT COUNT(*)
            FROM (	
                SELECT DISTINCT student_id
                FROM expression
                WHERE course_id = {0}
                AND UNIX_TIMESTAMP(date_time) >= {1}
                AND UNIX_TIMESTAMP(date_time) <= {2}
            ) tb1
        '''.format(course_id, datetime_start, datetime_end)
        student_num = db.session.execute(sql1).first()[0]

        sql2 = '''
            SELECT COUNT(*)
            FROM expression
            WHERE course_id = {0} 
            AND UNIX_TIMESTAMP(date_time) >= {1}
            AND UNIX_TIMESTAMP(date_time) <= {2}
        '''.format(course_id, datetime_start, datetime_end)
        expression_num = db.session.execute(sql2).first()[0]

        sql3 = '''
            SELECT SUM(grade)
            FROM expression
            WHERE course_id = {0}
            AND UNIX_TIMESTAMP(date_time) >= {1}
            AND UNIX_TIMESTAMP(date_time) <= {2}
        '''.format(course_id, datetime_start, datetime_end)
        if expression_num:
            average_grade = db.session.execute(sql3).first()[0] / expression_num
        else:
            average_grade = 0


        sql4 = '''
            SELECT grade
            FROM expression
            WHERE course_id = {0}
            AND UNIX_TIMESTAMP(date_time) >= {1}
            AND UNIX_TIMESTAMP(date_time) <= {2}
        '''.format(course_id, datetime_start, datetime_end)
        grades = db.session.execute(sql4)
        variance = 0
        for grade in grades:
            dif = abs(grade[0] - average_grade)
            variance += dif * dif
        response_data["student_num"] = str(student_num)
        response_data["expression_num"] = str(expression_num)
        response_data["average_grade"] = str(average_grade)
        response_data["variance"] = str(variance)

        # 计算各表情人数
        sql5 = '''
                SELECT COUNT(*) number, grade
                FROM expression
                WHERE course_id = {0}
                AND UNIX_TIMESTAMP(date_time) >= {1}
                AND UNIX_TIMESTAMP(date_time) <= {2}
                GROUP BY grade
            '''.format(course_id, datetime_start, datetime_end)
        number_of_grade = db.session.execute(sql5)
        for grade in range(1, 7):
            response_data["number_of_grade{0}".format(grade)] = str(0)
        for row in number_of_grade:
            response_data["number_of_grade{0}".format(row.grade)] = str(row.number)

        # 输出
        if return_type == 'json':
            return jsonify({"status": "success", "data": response_data})
        elif return_type == 'excel':
            path = "./temporary_file/statistic.xls"
            workbook = xlwt.Workbook(encoding='utf-8')
            worksheet = workbook.add_sheet('班级评价表', cell_overwrite_ok=True)
            i = 0
            for key, value in response_data.items():  # 将字典内容写入excel
                worksheet.write(i, 0, key)
                worksheet.write(i, 1, value)
                i += 1
            workbook.save(path)
            return send_file(path, as_attachment=True)
        else:
            return jsonify({"status": "error", "data": {"info": "返回类型错误!"}})
    except Exception as result:
        return jsonify({"status": "error", "data": {"info": str(result)}})


@bp.route('/query_excel', methods=['POST'])
def teacher_query_excel():
    return '1'
