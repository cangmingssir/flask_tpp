# coding:utf-8
from flask_restful import Resource, fields, marshal_with

from mainApp import dao
from mainApp.models import Letter


class CityApi(Resource):
    #城市的字段
    city_fields = {"id":fields.Integer,
                   'parentId':fields.Integer,
                   'regionName':fields.String,
                   'cityCode':fields.Integer,
                   'pinYin':fields.String}

    #城市字母的输出字段
    #value_fields={"A":fields.Nested(city_fields) for }
    value_fields = {}

    out_fields = {"returnCode":fields.String(default=0),
                  "returnValue":fields.Nested(value_fields)}
    @marshal_with(out_fields)
    def get(self):
        #获取所有城市字母对象集合
        letters = dao.queryAll(Letter)
        returnValue = {}
        for letter in letters:
            #向value_fields类属性中添加字段
            self.value_fields[letter.name]=fields.Nested(self.city_fields)
            #letter.citys是字母对象的城市对象集合
            returnValue[letter.name]=letter.citys
        print(returnValue)
        return {'returnValue':returnValue}