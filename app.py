from flask import Flask, request, jsonify, json, g
from flask_migrate import Migrate
import config
from apps import student_bp, teacher_bp, admin_bp, login_bp
from exts import db, mail
from models import LoginModel

app = Flask(__name__)
app.config.from_object(config)  # 导入配置
db.init_app(app)  # 绑定数据库
mail.init_app(app)  # 绑定邮箱
migrate = Migrate(app, db)  # 数据库更新工具

# 蓝图组装
app.register_blueprint(student_bp)
app.register_blueprint(teacher_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(login_bp)


@app.route("/")
def index() -> str:
    return "主页"


@app.before_request
def before_request():
    if len(request.path) >= 6 and request.path[:6] == "/login":
        return None  # 有问题还
    try:
        token = request.headers.get("token")
        if not token:
            return jsonify({"status": "error", "data": {"info": "请先登录"}}), 401
        user = LoginModel.query.filter_by(token=token).first()
        if user:
            g.user_id = user.user_id
            g.user_type = user.user_type
            return None
        else:
            return jsonify({"status": "error", "data": {"info": "登陆信息失效! 您可能在其他设备登陆!"}}), 401
    except Exception as result:
        return jsonify({"status": "error", "data": {"info": str(result)}})


@app.route("/logout", methods=["post"])
def logout() -> json:
    logout_account = LoginModel.query.filter_by(user_id=g.user_id,
                                                user_type=g.user_type).first()
    if logout_account:
        db.session.delete(logout_account)
        db.session.commit()
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "data": {"info": "理论上不会出这个错"}}), 401


if __name__ == '__main__':
    app.run()
