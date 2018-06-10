# coding:utf-8
#定义操作数据库的功能函数
from flask_sqlalchemy import BaseQuery

from mainApp.models import db


def queryOne(cls) -> BaseQuery:
    #返回基于某一类的查询
    return db.session.query(cls)

def queryAll(cls):
    #返回所有查询
    return queryOne(cls).all()


# def queryByName(cls,name):
#     return queryOne(cls).filter().first()


def getById(cls,id):
    try:
        return db.session.query(cls).get(int(id))
    except:
        return False

def save(obj):
    try:
        db.session.add(obj)
        db.session.commit()
    except:
        return False

    return True

def delete(obj) -> bool:
    try:
        db.session.delete(obj)
        db.session.commit()
    except:
        return False
    return True