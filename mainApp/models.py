# coding:utf-8
# 声明数据库中表对应的模型类
from datetime import datetime

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Text, Enum, Float
from sqlalchemy.orm import relationship, backref

# rom mainApp.ext import db


# migrate = Migrate()
# 创建数据库链接对象
db = SQLAlchemy()


def init_db(app):
    # 初始化数据库
    db.init_app(app)
    # 初始化数据库迁移方案
    Migrate(app, db)


# 字母模型，用于城市分类
class Letter(db.Model):
    __tablename__ = 't_letter'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    name = db.Column(String(10))


# 城市模型
class City(db.Model):
    __tablename__ = 't_city'
    id = Column(Integer, primary_key=True, autoincrement=True)
    parentId = Column(Integer, default=0)
    regionName = Column(String(50))
    cityCode = Column(Integer)
    pinYin = Column(String(100))

    letter_id = Column(Integer, ForeignKey(Letter.id))
    letter = relationship("Letter", backref=backref("citys", lazy=True))

#用户角色
class Role(db.Model):
    #用户角色
    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(20))
    rights = Column(Integer,default=1)


class Qx(db.Model):
    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(30))
    right = Column(Integer)

# 用户模型
class User(db.Model):
    __tablename__ = 't_user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), unique=True)
    password = Column(String(50))
    nickname = Column(String(20))
    email = Column(String(50), unique=True)
    phone = Column(String(12), unique=True)
    is_active = Column(Boolean, default=False)
    is_life = Column(Boolean, default=True)
    regist_time = Column(DateTime, default=datetime.now())
    last_login_time = Column(DateTime)
    # 新增头像属性
    photo_1 = Column(String(100), nullable=True)  # 原图
    phone_2 = Column(String(100), nullable=True)  # 小图

    #权限(被管理员授权)
    rights = Column(Integer,default=1)

    #用户角色
    role_id = Column(Integer,ForeignKey(Role.id))
    role =relationship('Role',backref=backref('users',lazy=True))

# 电影模型
class Movies(db.Model):
    # __tablename__='t_movie'
    id = Column(Integer, primary_key=True)
    showname = Column(String(50))  # 中文电影名
    shownameen = Column(String(50))  # 英文电影名
    director = Column(String(50))  # 导演
    leadingRole = Column(String(100))  # 主演演员信息
    type = Column(String(100))  # 电影类型
    country = Column(String(20))  # 国家
    language = Column(String(100))  # 语言
    duration = Column(Integer)  # 电影时长
    screeningmodel = Column(String(20))  # 放映模式(2D 3D 4D)
    openday = Column(DateTime)  # 上映时间
    backgroundpicture = Column(String(100))  # 背景图片
    flag = Column(Integer)  # 状态(热映 即将上映)
    isdelete = Column(Boolean, default=0)  # 是否删除


# 电影院模型
class Cinemas(db.Model):
    #__tablename__='t_cinemas'
    id=Column(Integer,primary_key=True)
    name = Column(String(50))       #名字
    city = Column(String(50))       #城市
    district = Column(String(50))     #区域
    address = Column(String(200))    #地址
    phone = Column(String(50))      #电话
    score = Column(Float(precision=1))         #影厅数量
    hallnum = Column(Float(10))         #评分
    servicecharge = Column(Float(precision=2))       #手续费
    astrict = Column(Integer)       #限购数量
    flag = Column(Boolean,default=True)     #状态(营业、休息)
    isdelete = Column(Boolean,default=True)     #是否删除


