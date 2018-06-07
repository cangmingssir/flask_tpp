# coding:utf-8
import uuid

from flask import request
from flask_mail import Message, Mail
from flask_restful import Resource, reqparse

from mainApp import helper, dao
import mainApp.ext
from mainApp.models import User



class UserApi(Resource):
    #定制输入字段
    parser=reqparse.RequestParser()

    parser.add_argument('username',dest='name',required=True,help='用户名不能为空')

    def post(self):
        #从基本的请求解析器中复制请求参数
        registParser = self.parser.copy()
        #再添加注册时使用
        registParser.add_argument('password', dest='pwd', required=True, help='口令不能为空')
        registParser.add_argument('email', required=True, help='邮箱不能为空')
        registParser.add_argument('phone', required=True, help='手机号不能为空')
        registParser.add_argument('nickname', required=True, help='昵称不能为空')

        #验证请求参数是否满足要求
        args = registParser.parse_args()
        u = User()
        u.name=args.get('name')
        u.nickname = args.get('nickname')
        u.email= args.get('email')
        u.phone = args.get('phone')
        #调用工具类的加密函数
        u.password=helper.md5_crypt(args.get('pwd').replace(' ',''))    #去除空格---replace
        print('dsfsdf',u)
        print(dao.save(u))
        if dao.save(u):
            helper.sendEmail(u)
            return {'status':200,
                    'msg':'用户注册成功！'}
        return {'status':201,
                    'msg':'用户注册失败！'}

    def get(self):
        #验证用户名是否已注册
        args = self.parser.parse_args()
        name=args.get('name')
        print('名字：',name)
        qs = dao.queryOne(User).filter(User.name==name)
        # print(qs)
        # print('sdfsdf',qs)
        if qs.count():
            return {'status':202,
                    'msg':'{} 用户名已被注册！'.format(name)}
        return {'status':200,
                    'msg':'{} 用户名可以使用！'.format(name)}

    # def put(self):
    #     #实现用户激活
    #     token = request.form.