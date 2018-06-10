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
    parser.add_argument('flag',type=int, required=True, help='必须指定影片类型')
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

    #查询方法
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

    #删除电影
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

    def post(self):
        movieActive = self.parser.copy()
        movieActive.add_argument('opt',required=True,help='请求类型不能为空')
        movieActive.remove_argument('flag')
        args =movieActive.parse_args()
        opt = args.get('opt')
        if opt == 'addmovie':
            return self.addMovie()
        elif opt == 'alertMovie':
            return self.alertMovie()



    #添加电影
    @check_login(QX.ADD_QX)
    def addMovie(self):
        return self.addAlertMovie(QX.ADD_QX)

    #修改电影
    def alertMovie(self):
        return self.addAlertMovie(QX.EDIT_QX)

    #添加修改电影的处理函数
    def addAlertMovie(self,qx):
        addmovieActive = self.parser.copy()
        addmovieActive.add_argument('id',type=int,required=True,help='电影编号不能为空')
        addmovieActive.add_argument('showname',required=True,help='电影名不能为空')
        addmovieActive.add_argument('shownameen',required=True,help='英文电影名不能为空')
        addmovieActive.add_argument('director',required=True,help='导演名不能为空')
        addmovieActive.add_argument('leadingRole',required=True,help='主演名不能为空')
        addmovieActive.add_argument('type',required=True,help='电影类型不能为空')
        addmovieActive.add_argument('country',required=True,help='所属国家不能为空')
        addmovieActive.add_argument('language',required=True,help='语言不能为空')
        addmovieActive.add_argument('duration',type=int,required=True,help='电影时间不能为空')
        addmovieActive.add_argument('screeningmodel',required=True,help='放映模式不能为空')
        addmovieActive.add_argument('openday',required=True,help='上映时间不能为空')
        addmovieActive.add_argument('backgroundpicture',required=True,help='背景图片不能为空')

        #验证请求参数
        args = addmovieActive.parse_args()
        movies_id = args.get('id')
        movies = dao.getById(Movies, movies_id)
        #判断用户是否执行修改权限
        if qx == QX.EDIT_QX:
            #print(movies.showname)
            #判断movies数据库中是否存在该电影，存在则判断为修改影片，否则为新增影片
            if not movies:
                return {'msg':'您所修改的电影不存在'}
        # 判断用户是否执行添加权限
        elif qx == QX.ADD_QX:
            if movies:
                return {'msg':'您所添加的电影已存在'}
            movies=Movies()
        #args是一个输入字段的字典
        for key,value in args.items():
            #判断key是否是movies的字段属性
            if hasattr(movies,key):
                print(key, ':', value)
                setattr(movies,key,value)
        # print('主演:',movies.leadingRole)
        # print('保存电影',dao.save(movies))
        if dao.save(movies):
            return {'msg':'{} 电影保存成功！'.format(movies.showname)}
        return {'msg':'电影保存失败，请检查必备属性是否输入'}
