# coding:utf-8
import json
import pymysql

with open('citys.json','rb') as f:
    citys = json.load(f)
    print(type(citys))
    print(citys)

    #链接数据库
    db = pymysql.connect(host='localhost',
                         port=3306,
                         user='root',
                         password='root',
                         db='tpp',
                         charset='utf8')
    print('数据库链接成功!')
    #创建游标对象
    cursor = db.cursor()

    values = citys['returnValue']
    for letter in values.keys():
        cursor.execute('insert t_letter(name) values(%s)',letter)
        #db.commit()

        cursor.execute('select id from t_letter where name=%s',letter)
        letter_id = cursor.fetchone()[0]

        print('添加成功!'+letter,letter_id,cursor.rowcount)
        for city in values.get(letter):

            cursor.execute('insert t_city values(%s,%s,%s,%s,%s,%s)',
                           (city.get('id'),
                            city.get('parentId'),
                            city.get('regionName'),
                            city.get('cityCode'),
                            city.get('pinYin'),
                            letter_id))
    db.commit()