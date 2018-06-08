# coding:utf-8
import uuid

from celery import Celery
from flask import request
from flask_mail import Message

import mainApp
from mainApp import helper, dao
from mainApp.helper import md5_crypt
from mainApp.models import User


celery = Celery('tasks',broker='redis://:109321@10.35.163.24:6379/12',
                include=['manage'])


@celery.task
def sendMail(uId):
    try:
        import manage
    except:
        pass
    global manage
    with manage.app.test_request_context():
        user = dao.getById(User,uId)
        # 生成token
        token = md5_crypt(str(uuid.uuid4()))
        print('我得token', token)
        # 将token设置到redis缓存中
        mainApp.ext.cache.set(token, user.id, timeout=10 * 60)  # 允许10分钟来激活用户
        print('redis的token：', mainApp.ext.cache.get(token))
        # 激活的链接
        active_url = request.host_url + 'account/?opt=active&token=' + token
        # 发送邮件
        # 创建msg对象
        msg = Message(subject='淘票票激活用户',
                      recipients=[user.email],  # 必须是列表，可添加多个元素
                      sender='mu_tongwu@163.com')
        # 编辑内容
        msg.html = '<h1>{} 注册成功！</h1><br/><h3>请先<a href={}>激活</a>注册账号</h3><br/>' \
                   '<h3>可将下面地址复制到浏览器中进行激活</h3><p>{}</p>'. \
            format(user.nickname, active_url, active_url)

        # 发送邮件
        try:
            mainApp.ext.mail.send(msg)
            print('邮件已发送')
        except Exception as e:
            print(e)
            print('邮件发送失败')


if __name__ == '__main__':
    celery.worker_main()