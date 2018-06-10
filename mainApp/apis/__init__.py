# coding:utf-8
from flask_restful import Api

from mainApp.apis.account_api import AccountApi
from mainApp.apis.cinemas_api import CinemasApi
from mainApp.apis.city_api import CityApi
from mainApp.apis.movies_api import MoviesApi
from mainApp.apis.user_api import UserApi

api = Api() #创建RESTful的Api对象

def init_api(app):
    api.init_app(app)

#向api接口中添加资源（Resource）
api.add_resource(CityApi,'/city/')
api.add_resource(UserApi,'/user/')
api.add_resource(AccountApi,'/account/')
api.add_resource(MoviesApi,'/movies/')
api.add_resource(CinemasApi,'/cinemas/')