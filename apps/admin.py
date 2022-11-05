# -*- coding: utf-8 -*-
# @Time : 10/26/22 1:54 PM
# @Author : ZhuFujun
# @File : admin.py
# @Software : PyCharm


from flask import Blueprint, request, jsonify, json, send_file, g
from models import StudentModel, TeacherModel, AdminModel
from exts import db

bp = Blueprint("admin", __name__, url_prefix="/admin")


# 参数: account_type, page_size, which_page
@bp.route('/query', methods=['GET'])
def admin_query() -> json:
    try:
        # 从查询字符串得到数据
        account_type = request.args.get("account_type")
        page_size = request.args.get("page_size")
        which_page = request.args.get("which_page")
        if not account_type or not page_size or not which_page:
            return jsonify({"status": "error", "data": {"info": "参数空缺!"}})
        page_size = int(page_size)
        which_page = int(which_page)
        sql = '''
            SELECT *
            FROM {0}
            LIMIT {1},{2}
        '''.format(account_type, (which_page - 1) * page_size, page_size)
        account_list = db.session.execute(sql)
        if account_type == "student":
            column_name = StudentModel.__table__.columns.keys()
        elif account_type == "teacher":
            column_name = TeacherModel.__table__.columns.keys()
        elif account_type == "admin":
            column_name = AdminModel.__table__.columns.keys()
        contents = []
        for account in account_list.fetchall():
            content = {}
            for i, val in enumerate(account):
                if val:
                    content[column_name[i]] = val
                else:
                    content[column_name[i]] = "null"
            contents.append(content)
        return jsonify({"status": "success", "data": {"contents": contents}})
    except Exception as result:
        return jsonify({"status": "error", "data": {"info": str(result)}})


# 参数:
@bp.route('/add_account', methods=['POST'])
def admin_add_account() -> json:
        if g.user_type != 'admin':
            return jsonify({"status": "error", "data": {"info": "您不是管理员, 请自重!"}})
        try:
            data = request.get_data()
            data = json.loads(data)
            account_type = data['account_type']
            if account_type == 'student':
                user = StudentModel()
            elif account_type == 'teacher':
                user = TeacherModel()
            elif account_type == 'admin':
                user = AdminModel()
            else:
                return jsonify({"status": "error", "data": {"info": "错误的用户种类"}})
            for key, value in data.items():
                if hasattr(user, key):
                    user.__setattr__(key, value)
            db.session.add(user)
            db.session.commit()
            return jsonify({"status": "success", "data": {"user_id": user.id}})
        except Exception as result:
            return jsonify({"status": "error", "data": {"info": str(result)}})


# 参数:
@bp.route('/delete_account', methods=['POST'])
def admin_delete_account() -> json:
        if g.user_type != 'admin':
            return jsonify({"status": "error", "data": {"info": "您不是管理员, 请自重!"}})
        try:
            data = request.get_data()
            data = json.loads(data)
            account_type, user_id = data['account_type'], data['user_id']
            if account_type == 'student':
                user = StudentModel.query.filter_by(id=user_id).first()
            elif account_type == 'teacher':
                user = TeacherModel.query.filter_by(id=user_id).first()
            elif account_type == 'admin':
                user = AdminModel.query.filter_by(id=user_id).first()
            else:
                return jsonify({"status": "error", "data": {"info": "错误的用户种类"}})
            if user:
                db.session.delete(user)
                db.session.commit()
                return jsonify({"status": "success"})
            else:
                return jsonify({"status": "error", "data": {"info": "没有该用户"}})

        except Exception as result:
            return jsonify({"status": "error", "data": {"info": str(result)}})
