# _*_ coding:utf-8 _*_
# filename : __init__.py

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from config import config

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    # 注册蓝本
    from .webapp.main import main as main_blueprint
    from .webapp.author import author as author_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(author_blueprint)
    
    return app

