# _*_ coding:utf-8 _*_
# filename : __init__.py

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from config import config
from flask_login import LoginManager
from flask_pagedown import PageDown
bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'user.login'
pagedown = PageDown()


def create_app(config_name):
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)

    # 注册蓝本
    from .webapp.main import _main as main_blueprint
    from .webapp.user import _user as user_blueprint
    from .webapp.admin import _admin as admin_blueprint

    app.register_blueprint(main_blueprint, url_prefix='/main')
    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    return app

