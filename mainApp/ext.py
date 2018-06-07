# coding:utf-8
# 集成第三方包
from flask_cache import Cache
from flask_session import Session

from mainApp.apis import init_api
from mainApp.models import init_db
from flask_mail import Mail


mail=Mail()

cache = Cache(config={'CACHE_TYPE':'redis',
                                  'CACHE_REDIS_HOST':'10.35.163.24',
                                  'CACHE_REDIS_POST':'6379',
                                  'CACHE_REDIS_DB':12,
                                  'CACHE_REDIS_PASSWORD':109321})

se = Session()

def init_ext(app):
    #初始化数据库
    init_db(app)
    #初始化api接口
    init_api(app)

    #初始化mail
    mail.init_app(app)

    #初始化cache缓存
    cache.init_app(app)

    #初始化session
    se.init_app(app)
