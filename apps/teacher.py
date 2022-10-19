# -*- coding: utf-8 -*-
#@Time : 10/10/22 11:17 PM
#@Author : 知北游
#@File : teacher.py
#@Software : PyCharm

from flask import Blueprint,request,jsonify,json,send_file
from models import User, Expression, Course
from exts import db
from verify import tokenVerify
import xlwt # excel操作

bp = Blueprint("teacher", __name__, url_prefix="/teacher")


# post到 IP/teacher/enter_course json包含token,course_code
@bp.route('/enter_course', methods=['GET'])
def teacher_enter_course()->json:
    try:
        token = request.headers.get("token")
        user = tokenVerify(token, "teacher")
        if(user == None):
                return jsonify({"status": "error", "data": {"info": "没有这个教师或您不是教师!"}})
        course_code = request.args.get("course_code")
        print(token)
        course = Course.query.filter_by(course_code=course_code).first()
        if course != None:
            info = "老师:"+ user.email+ "  进入课程:"+ course.course_name+ "  课程Code:"+ course_code
            print(info)
            db.session.commit()
            return jsonify({"status": "success", "data": {"course_id":str(course.id), "info": info}})
        else:
            print(course_code)
            return jsonify({"status": "error", "data": {"info": "没有这个课程!"}})
    except (Exception) as result:
        return jsonify({"status": "error", "data": {"info": str(result)}})  # 其他错误 直接塞到json里返回


# post到 IP/teacher/query json包含token, datetime_start, datetime_end, course_id, return_type = "json" / "excel"
@bp.route('/query', methods = ['GET'])
def teacher_query()->json:
    try:
        token = request.headers.get("token")
        user = tokenVerify(token, "teacher")
        if(user == None):
                return jsonify({"status": "error", "data": {"info": "没有这个教师或您不是教师!"}})
        # 从查询字符串得到数据
        datetime_start = request.args.get("datetime_start")
        datetime_end = request.args.get("datetime_end")
        course_id = request.args.get("course_id")
        return_type = request.args.get("return_type")

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
        if student_num == 0: # 没有表情!
            expression_num, average_grade, variance = [0]*3
        else:
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
            average_grade = db.session.execute(sql3).first()[0] / expression_num

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
                variance += dif*dif
        if return_type == 'json':
            return jsonify({"status": "success", "data": {"student_num":str(student_num),
                                                          "expression_num": str(expression_num),
                                                          "average_grade": str(average_grade),
                                                          "variance": str(variance)
                                                          }})
        elif return_type == 'excel':
            path = "./temporary_file/statistic.xls"
            workbook = xlwt.Workbook(encoding='utf-8')
            worksheet = workbook.add_sheet('班级评价表', cell_overwrite_ok=True)
            elems = ["student_num", "expression_num", "average_grade", "variance"]
            values = [student_num, expression_num, average_grade, variance]
            for i in range(4):
                worksheet.write(0, i, elems[i])
                worksheet.write(1, i, values[i])
            workbook.save(path)
            return send_file(path, as_attachment = True)
        else:
            return jsonify({"status": "error", "data": {"info": "返回类型错误!"}})


    except (Exception) as result:
        return jsonify({"status": "error", "data": {"info": str(result)}})  # 其他错误 直接塞到json里返回



@bp.route('/query_excel', methods = ['POST'])
def teacher_query_excel():
    return '1'