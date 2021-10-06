# -*- coding = utf-8 -*-
# @Time : 2021/9/28 18:13
# @Author : 羊来
# @File : test_Click.py
# @Software: PyCharm
import click
from app import app,User,Movie
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_ECHO'] = True
app.config.from_object(config)
db = SQLAlchemy()

# db.create_all()  # 全局的两个变量移动到这个函数内
# name = 'Grey Li'
# movies = [{'title': 'Mahjong', 'year': '1996'},
#           {'title': 'Swallowtail Butterfly', 'year': '1996'},
#           {'title': 'King of Comedy', 'year': '1999'},
#           {'title': 'Devils on the Doorstep', 'year': '1999'},
#           {'title': 'WALL-E', 'year': '2008'},
#           {'title': 'The Pork of Music', 'year': '2012'},]
# user = User(name=name)
# db.session.add(user)
# for m in movies:
#     t = m['title']
#     y = m['year']
#     print(t)
#     print(y)
#     try:
#         movie = Movie(title=t, year=y)
#         db.session.add(movie)
#     except:
#         print("sth wrong")

# movies = Movie.query.all()
# for movie in movies:
#     print(movie.id)
#     print(movie.title)
#     try:
#         if movie.title == "My Neighbor Totoro":
#             db.session.delete(movie)
#             print("删除成功")
#     except:
#         print("Sth Wrong")

movie = Movie.query.get(4)
db.session.delete(movie)
db.session.commit()
# db.session.commit()
# click.echo('Done.')
