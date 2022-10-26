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
    try:
        pass
    except Exception as result:
        return jsonify({"status": "error", "data": {"info": str(result)}})


# 参数:
@bp.route('/delete_account', methods=['POST'])
def admin_delete_account() -> json:
    try:
        pass
    except Exception as result:
        return jsonify({"status": "error", "data": {"info": str(result)}})
