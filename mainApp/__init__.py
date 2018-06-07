# coding:utf-8
from flask import Flask
from mainApp import settings
from mainApp.ext import init_ext


def create_app():
    #创建app对象
    app = Flask(__name__)

    app.config.from_object(settings.Config)

    #初始化第三方插件
    init_ext(app)

    return app