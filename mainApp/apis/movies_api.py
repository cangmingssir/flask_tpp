# coding:utf-8
from flask import request, session
from flask_restful import Resource, reqparse, fields, marshal_with
from flask_sqlalchemy import BaseQuery

from mainApp import dao
from mainApp.models import Movies, User, Qx
from mainApp.settings import QX

#装饰器函数，用于做权限判断
def check_login(qx):
    def check(fun):
        def wrapper(*args,**kwargs):
            print('-check login-')
            token = request.args.get('token')
            user_id = session.get(token)
            loginUser = dao.getById(User,user_id)
            if not user_id:
                return {'msg':'用户必须先登录'}
            if loginUser.rights & qx == qx:
                return fun(*args,**kwargs)
            else:
                qxObj = dao.queryOne(Qx).filter(Qx.right==qx).first()
                return {'msg':'用户没有{}权限'.format(qxObj.name)}
        return wrapper
    return check


class MoviesApi(Resource):
    # 定制输入的参数
    parser = reqparse.RequestParser()
    parser.add_argument('flag', required=True, help='必须指定影片类型', type=int)
    parser.add_argument('city', default='')
    parser.add_argument('region', default='')
    parser.add_argument('orderby',default='openday')
    parser.add_argument('sort',type=int,default = 1)
    parser.add_argument('page', help='页码必须是数值',default= 1, type=int)
    parser.add_argument('limit', help='每页显示的大小必须是大小', default=10,type=int)

    # 定制输入字段
    out_fields = {
        'returnCode': fields.String(default='0'),
        'returnValue': fields.Nested({
            "backgroundPicture": fields.String(attribute='backgroundpicture'),
            "country": fields.String,
            "director": fields.String,
            "showName": fields.String(attribute='showname'),
            "showNameEn": fields.String(attribute='shownameen'),
            'openTime':fields.DateTime(attribute='openday')
        })
    }

    @marshal_with(out_fields)
    def get(self):
        # 验证请求参数
        args = self.parser.parse_args()
        movies:BaseQuery = dao.queryOne(Movies).filter(Movies.flag == args.get('flag'))
        print(movies.all())

        sort = args.get('sort')
            #排序
        movies = movies.order_by(('-' if sort==1 else '')+args.get('orderby'))
        #分页
        pager = movies.paginate(args.get('page'),args.get('limit'))

        return {'returnValue': pager.items}

    @check_login(QX.DELETE_QX)
    def delete(self):
        mid = request.args.get('mid')
        movie = dao.getById(Movies, mid)
        if not movie:
            return {'msg': '你要删除的影片资源不存在'}
        dao.delete(movie)
        return {'msg': '删除 {} 影片成功'.format(movie.showname)}
        # mid = request.args.get('mid')
        # # 从session中获取登录用户的token
        # user_id = session.get(request.args.get('token'))
        # if not user_id:
        #     return {'msg':'请先登录'}
        # loginUser = dao.getById(User,user_id)
        # if loginUser.rights&QX.DELETE_QX == QX.DELETE_QX:
        #     movie = dao.getById(Movies,mid)
        #     if not movie:
        #         return {'msg':'你要删除的影片资源不存在'}
        #     dao.delete(movie)
        #     return {'msg':'删除 {} 影片成功'.format(movie.showname)}
        #
        # return ({'msg':'您没有VIP权限，请开通VIP功能'})

