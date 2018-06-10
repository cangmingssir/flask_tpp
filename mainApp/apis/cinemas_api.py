# coding:utf-8
from flask import request, session
from flask_restful import Resource, reqparse, fields, marshal_with

from mainApp import dao
from mainApp.models import Cinemas, User, Qx
from mainApp.settings import QX


def check_login(qx):
    def check(fn):
        def wrapper(*args,**kwargs):
            token = request.args.get('token')
            if not token:
                token = request.form.get('token')
            user_id = session.get(token)
            loginUser = dao.getById(User,user_id)
            if not loginUser:
                return {'msg':'请先登录！'}
            if loginUser.rights & qx == qx:
                return fn(*args,**kwargs)
            qxObj = dao.queryOne(Qx).filter(Qx.right==qx).first()
            return {'msg':'您没有 {} 权限'.format(qxObj.name)}
        return wrapper
    return check



class CinemasApi(Resource):

    #定义输入字段
    parser = reqparse.RequestParser()
    parser.add_argument('token')
    parser.add_argument('opt',required=True)
    parser.add_argument('name',help='电影院名称')
    parser.add_argument('city',help='影院城市不能为空')
    parser.add_argument('district',help='城市区域不能为空')
    parser.add_argument('sort',type=int,default=1)
    parser.add_argument('orderby',default='hallnum')
    parser.add_argument('limit',type=int,default=10)
    parser.add_argument('page',type=int,default=1)


    #定义输出字段

    cinemas_fields = {
            'id':fields.Integer,
            'name':fields.String,
            'city':fields.String,
            'district':fields.String,
            'address':fields.String,
            'phone':fields.String,
            'score':fields.Float,
            'hallnum':fields.Integer,
            'servicecharge':fields.Float,
            'astrict':fields.Integer,
            'flag':fields.Boolean,
            'isdelete':fields.Boolean
        }

    out_fields={
        'returnValue':fields.Nested(cinemas_fields)
    }

    def selectCinemas(self,cinemas):
        args=self.parser.parse_args()
        sort = args.get('sort')
        cinemas = cinemas.order_by(('-' if sort ==1 else '')+args.get('orderby'))
        pager = cinemas.paginate(args.get('page'),args.get('limit'))

        return {'returnValue':pager.items}

    @marshal_with(out_fields)
    def get(self):
        #验证请求参数
        args=self.parser.parse_args()
        opt =args.get('opt')
        city = args.get('city')
        district = args.get('district')
        #用于查询某城市区域的影城信息
        if opt == 'cityAndDistrict':
            if city and district:
                cinemas=dao.queryOne(Cinemas).filter(Cinemas.city==city,
                                                 Cinemas.district==district)
                if not cinemas.count():
                    return {'msg':'该地区没有电影院'}
                self.selectCinemas(cinemas)
            return {'msg':'城市和城区区域不能为空'}
        elif opt == 'city':
            if city:
                cinemas=dao.queryOne(Cinemas).filter(Cinemas.city==city)
                if not cinemas.count():
                    return {'msg':'该城市没有电影院'}
                self.selectCinemas(cinemas)
            return {'msg':'搜索城市不能为空'}
        else:
            cinemas=dao.queryAll(Cinemas)
            self.selectCinemas(cinemas)


    @check_login(QX.DELETE_QX)
    def delete(self):
        cid = request.args.get('cid')
        cinemas = dao.getById(Cinemas,cid)
        if not cinemas:
            return {'msg':'您删除的影院不存在'}
        if not dao.delete(cinemas):
            return {'msg':'删除失败'}
        return {'msg':'删除成功'}

    def post(self):
        pass


