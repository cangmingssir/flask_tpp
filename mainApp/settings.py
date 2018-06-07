# coding:utf-8
import os

from redis import Redis

# 配置头像的存储路径
IMAGE_SAVE = os.path.dirname(os.path.abspath(__name__))
MEDIA_DIR = os.path.join(IMAGE_SAVE, 'mainApp/static/uploads')


class Config():
    ENV = 'development'
    DEBUG = True
    #配置安全的密钥
    SECRET_KEY = '348r7683kjefkjqh4g$%$'

    #配置数据库链接
    SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:root@localhost:3306/tpp'
    SQLALCHEMY_TRACK_MODIFICATIONS=False

    #配置邮箱
    MAIL_SERVER = 'smtp.163.com'    #邮箱服务器
    MAIL_USERNAME = 'mu_tongwu@163.com'
    MAIL_PASSWORD='wupeng109321'   #授权码

    #配置Session的redis服务
    SESSION_TYPE = 'redis'
    SESSION_REDIS = Redis(host='10.35.163.24',port=6379,db=10,password='109321')




