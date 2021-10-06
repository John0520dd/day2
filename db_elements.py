# -*- coding = utf-8 -*-
# @Time : 2021/9/28 17:02
# @Author : 羊来
# @File : db_elements.py
# @Software: PyCharm
from app import user,movie
from flask import Flask, request, json, Response
from flask_sqlalchemy import SQLAlchemy
import config
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_ECHO'] = True
app.config.from_object(config)
db = SQLAlchemy(app)


# 1.插入数据
u1 = user(
    name = 'Hannibal'
)

m1 = movie(
    title='Ok',
    year='1932'
)
db.session.add(u1)
db.session.add(m1)
db.session.commit()

# movie = movie.query.first()
#
# print(movie.name)
# print(movie.id)
#
# user = user.query.first()
# print(user.id,user.title,user.year)