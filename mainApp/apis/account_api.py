# coding:utf-8
import os
import uuid
from datetime import datetime

from flask import request, session
from flask_restful import Resource, reqparse, fields, marshal
from werkzeug.datastructures import FileStorage

import mainApp.ext
from mainApp import dao, helper, settings
from mainApp.models import User
from mainApp.helper import md5_crypt
import mainApp.dao


class AccountApi(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('opt', required=True, help='没有opt操作')

    # parser.add_argument('token')
    def get(self):
        # 从请求参数中获取opt和token参数值
        # 如果opt为avtive，则从redis缓存中查询token对应的user.id
        # 再通过 user.id 查询数据库中用户，最后更新用户的is_active状态
        # token = mainApp.ext.cache.get(str(request.args.get('token')))
        # 通过get请求获取opt数据

        args = self.parser.parse_args()
        opt = args.get('opt')
        # print('类型：', type(opt))
        # print(opt)
        # opt为请求状态
        if opt == 'active':
            activeParser = self.parser.copy()
            activeParser.add_argument('token', required=True, help='没有token')
            args = activeParser.parse_args()
            token = args.get('token')
            user_id = mainApp.ext.cache.get(token)
            if user_id:
                user = dao.getById(User, user_id)
                # print('用户',user)
                # print(type(user))
                user.is_active = True
                dao.save(user)
                return {'msg': '{} 激活成功'.format(user.nickname)}
            else:
                # 重新申请激活
                reactive_url = request.host_url + 'account/?opt=reactive'
                return {'msg': '激活超时，请重新激活'+reactive_url}
        elif opt == 'reactive':
            return self.reactive()

        elif opt == 'login':
            return self.login()

        elif opt == 'logout':
            return self.logout()

    # 重新申请用户激活
    def reactive(self):
        reactiveParser = self.parser.copy()
        reactiveParser.add_argument('email', required=True, help='邮箱不能为空')
        args = reactiveParser.parse_args()
        email = args.get('email')
        qs = dao.queryOne(User).filter(User.email == email)
        print('我得qs用户',qs.first())
        if not qs.count():
            return {'status': 505, 'msg': email + '邮箱未被注册'}
        # 重新发送邮件,sendEmail封装的是发送邮件的代码
        helper.sendEmail(qs.first())

        return {'msg': '重新申请用户激活，请查收邮箱进行激活'}

    # 定义登录
    def login(self):

        activeParser = self.parser.copy()
        activeParser.add_argument('Token')
        activeParser.add_argument('username', dest='name', required=True, help='用户名真的不能为空')
        activeParser.add_argument('password', dest='pwd', required=True, help='密码不能为空')

        args = activeParser.parse_args()
        print(session.get(args.get('Token')))
        if session.get(args.get('Token')):
            print('dfdfdfdfdfdf')
            return {'msg': '还想通过直接输入网页地址登录？'}


        name = args.get('name')
        print(name)
        # 将获取的用户输入密码加密，用于和数据库中密码相比较
        pwd = md5_crypt(args.get('pwd'))
        qs = dao.queryOne(User).filter(User.name == name,
                                       User.password == pwd)
        print('进来了峨眉')
        if not qs.count():
            return {'status':600,'msg': '您的用户名或口令有误'}
        else:
            qs:User = qs.first()
            if not qs.is_life:
                return {'status':700,'msg':'该用户已注销'}
            if qs.is_active:
                # 生成登录token，并将其存入至session中
                loginToken = md5_crypt(str(uuid.uuid4()))
                print(loginToken)
                session[loginToken] = qs.id
                print('这是进来的user_id',qs.id)
                qs.last_login_time=datetime.now()
                dao.save(qs)
                print('-----------')
                out_user_fields = {
                    'name': fields.String,
                    'email': fields.String,
                    'phone': fields.String,
                    'photo': fields.String(attribute='photo_1')
                }
                out_fieleds = {
                    'msg': fields.String,
                    'data': fields.Nested(out_user_fields),
                    'access_token': fields.String
                }
                data = {'msg': '登录成功',
                        'data': qs,
                        'access_token':loginToken}
                print('========')
                return marshal(data,out_fieleds)
            return {'msg':'该用户未被激活'}

    #退出登录
    def logout(self):
        logoutactiveParser=self.parser.copy()
        logoutactiveParser.add_argument('Token',required=True,help='token不能为空')
        args = logoutactiveParser.parse_args()
        logintoken = args.get('Token')
        user_id = session.get(logintoken)
        if not user_id:
            return {'status':701,'msg':'用户未登录，请先登录！'}
        user = dao.getById(User,user_id)
        if not user:
            return {'status':702,'msg':'用户退出失败，token无效！'}
        session.pop(logintoken)
        #session.clear()
        return {'status':200,'msg':'退出成功！'}

    # def delete(self):
    #     session.clear()
    #     return {'msg':'dfdfdfdf'}



    def post(self):
        #定义输入字段
        myImageactice = self.parser.copy()
        myImageactice.remove_argument('opt')    #移除opt的输入字段
        myImageactice.add_argument('img',type=FileStorage,location='files',
                                   required=True,help='必须要上传图片文件')
        myImageactice.add_argument('Token')
        args = myImageactice.parse_args()
        token = args.get('Token')
        if not token:
            return {'msg':'请登录！'}

        user_id = session.get(token)
        user = dao.getById(User,user_id)
        if not user:
            return {'msg':'Token无效,请确定您是否登录'}

        #获取image对象
        upImage:FileStorage = args.get('img')
        print('上传图片的文件名：',upImage.filename)
        #重新命名文件名
        newImage = str(uuid.uuid4()).replace('-','')+'.'+upImage.filename.split('.')[-1]
        print('新的文件名',newImage)
        upImage.save(os.path.join(settings.MEDIA_DIR,newImage))
        user.photo_1 = newImage
        dao.save(user)

        #定义输出字段
        out_image_fields={
            'msg':fields.String('文件上传成功!'),
            'data':fields.String,
            'access_token':fields.String
        }

        data={'data':newImage,
              'access_token':token}
        return marshal(data,out_image_fields)

    # 定制输入字段
    # parser = reqparse.RequestParser()
    # parser.add_argument('username', dest='name', required=True, help='用户名真的不能为空')
    # parser.add_argument('password', dest='pwd', required=True, help='密码不能为空')

    # 验证登录是否成功
    # def post(self):
    #     if session.get('loginToken'):
    #         return {'msg': '还想通过直接输入网页地址登录？'}
    #     args = self.parser.parse_args()
    #     name = args.get('name')
    #     # 将获取的用户输入密码加密，用于和数据库中密码相比较
    #     pwd = md5_crypt(args.get('pwd'))
    #     qs = dao.queryOne(User).filter(User.name == name,
    #                                    User.password == pwd)
    #     if qs.count():
    #         # 生成登录token，并将其存入至session中
    #         loginToken = md5_crypt(str(uuid.uuid4()))
    #         session['loginToken'] = loginToken
    #         return {'msg': '{} 欢迎回家'.format(name)}
    #     return {'msg': '您的用户名或口令有误'}
    #
    # #退出登录
    # def delete(self):
    #     session.clear()
    #     return {'msg': '已退出登录'}
