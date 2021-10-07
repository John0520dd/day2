from flask import Flask,render_template
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_ECHO'] = True
app.config.from_object(config)
db = SQLAlchemy(app)


# @app.route('/')
# def index():
#     return render_template('index1.html',name = name,movies = movies)

class User(db.Model): # 表名将会是 user（自动生成，小写处理）
    id = db.Column(db.Integer, primary_key=True) # 主键
    name = db.Column(db.String(20)) # 名字

class Movie(db.Model):# 表名将会是movie
    id = db.Column(db.Integer, primary_key=True) # 主键
    title = db.Column(db.String(60)) # 电影标题
    year = db.Column(db.String(4)) # 电影年份

@app.context_processor
def inject_user(): # 函数名可以随意修改
    user = User.query.first()
    return dict(user=user) # 需要返回字典，等同于return {'user': user}

@app.route('/')
def index():
    # user = User.query.first() # 读取用户记录
    movies = Movie.query.all() # 读取所有电影记录
    # return render_template('index1.html', movies=movies)
    return render_template('index.html', movies=movies)

@app.errorhandler(404) # 传入要处理的错误代码
def page_not_found(e): # 接受异常对象作为参数
    # return render_template('404.html'), 404
    return render_template('404_1.html'), 404
    # test



if __name__ == '__main__':
    app.run(Debug=True)
