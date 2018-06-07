# coding:utf-8
from flask_restful import Resource, reqparse, fields, marshal_with
from flask_sqlalchemy import BaseQuery

from mainApp import dao
from mainApp.models import Movies


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
