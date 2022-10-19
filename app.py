from flask import Flask, jsonify, url_for, request, render_template
from flask_migrate import Migrate
import json
from models import User
import config
from apps import  student_bp, teacher_bp
from exts import db


app = Flask(__name__)
app.config.from_object(config) # 导入配置
db.init_app(app) # 绑定数据库
migrate = Migrate(app, db) # 数据库更新工具

# 蓝图组装
app.register_blueprint(student_bp)
app.register_blueprint(teacher_bp)




# post一个json, 包含 email, password, user_type 三项
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        data = request.get_data();
        if(data == None or len(data) == 0):
            return jsonify({"status":"error","data":{"info":"空内容"}})
        try:
            data = json.loads(data);
            print("登陆尝试: ", request.remote_addr,"\n用户数据",data)
            user = User.query.filter_by(email = data['email'],
                                        password = data['password'],
                                        user_type = data['user_type']).first()
            if user != None:
                return jsonify({"status":"success","data":{"token":str(user.id)}})
            else:
                return jsonify({"status":"error","data":{"info":"账号或密码错误"}})
        except (Exception) as result:
            return jsonify({"status":"error","data":{"info":str(result)}}) # 其他错误 直接塞到json里返回



@app.route("/")
def index():
    return "主页"


if __name__ == '__main__':
    app.run()
