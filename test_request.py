# -*- coding = utf-8 -*-
# @Time : 2021/10/3 23:22
# @Author : 羊来
# @File : test_request.py
# @Software: PyCharm
from flask import request, url_for, redirect, flash, render_template, Flask
from flask_sqlalchemy import SQLAlchemy

from app import user,movie
import config


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config.from_object(config)

db = SQLAlchemy(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST': # 判断是否是 POST 请求 # 获取表单数据
        title = request.form.get('title') # 传入表单对应输入字段的 name 值
        year = request.form.get('year') # 验证数据
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.') #显示错误提示
            return redirect(url_for('index')) # 重定向回主页 # 保存表单数据到数据库
            movie = Movie(title=title, year=year) # 创建记录
            db.session.add(movie) # 添加到数据库会话
            db.session.commit() # 提交数据库会话
            flash('Item created.') # 显示成功创建的提示
            return redirect(url_for('index')) # 重定向回主页

        # user = user.query.first()
        # movies = movie.query.all()
        # return render_template('index1.html', user=user, movies=movies)
