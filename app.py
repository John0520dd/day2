from flask import Flask,render_template,request,url_for,redirect,flash
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
import config
import click
from flask_login import LoginManager,UserMixin,login_user,login_required,logout_user

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_ECHO'] = True
app.config.from_object(config)
db = SQLAlchemy(app)
login_manager = LoginManager(app) # 实例化扩展类


# 这玩意到底加在哪
login_manager.login_view = 'hello'
# app.config['SECRET_KEY'] = 'dev'

# @app.route('/')
# def index():
#     return render_template('index1.html',name = name,movies = movies)

# class User(db.Model): # 表名将会是 user（自动生成，小写处理）
#     id = db.Column(db.Integer, primary_key=True) # 主键
#     name = db.Column(db.String(20)) # 名字

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20)) # 用户名
    password_hash = db.Column(db.String(128)) # 密码散列值

    def set_password(self, password): # 用来设置密码的方法，接受密码 作为参数
        self.password_hash = generate_password_hash(password) # 将生成的密码保持到对应字段

    def validate_password(self, password): # 用于验证密码的方法，接 受密码作为参数
        return check_password_hash(self.password_hash, password) # 返回布尔值

class Movie(db.Model):# 表名将会是movie
    id = db.Column(db.Integer, primary_key=True) # 主键
    title = db.Column(db.String(60)) # 电影标题
    year = db.Column(db.String(4)) # 电影年份

@app.context_processor
def inject_user(): # 函数名可以随意修改
    user = User.query.first()
    return dict(user=user) # 需要返回字典，等同于return {'user': user}

@app.route('/')
def hello():
    # user = User.query.first() # 读取用户记录
    movies = Movie.query.all() # 读取所有电影记录
    # return render_template('index1.html', movies=movies)
    return render_template('index.html', movies=movies)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST': # 判断是否是 POST 请求 # 获取表单数据
        title = request.form.get('title') # 传入表单对应输入字段的 name 值
        year = request.form.get('year') # 验证数据
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.') # 显示错误提示
            return redirect(url_for('index')) # 重定向回主页

        # 保存表单数据到数据库
        movie = Movie(title=title, year=year) # 创建记录
        db.session.add(movie) # 添加到数据库会话
        db.session.commit() # 提交数据库会话
        flash('Item created.') # 显示成功创建的提示
        return redirect(url_for('hello')) # 重定向回主页

        user = User.query.first()
        movies = Movie.query.all()
    return render_template('index.html', user=user, movies=movies)


@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST': # 处理编辑表单的提交请求
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id)) # 重定向回对应的编辑页面

        movie.title = title # 更新标题
        movie.year = year # 更新年份
        db.session.commit() # 提交数据库会话
        flash('Item updated.')
        return redirect(url_for('hello')) # 重定向回主页

    return render_template('edit.html', movie=movie) # 传入被编辑 的电影记录

@app.route('/movie/delete/<int:movie_id>', methods=['POST']) # 限定只接受 POST 请求
@login_required # 登录保护
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id) # 获取电影记录
    db.session.delete(movie) # 删除对应的记录
    db.session.commit() # 提交数据库会话
    flash('Item deleted.')
    return redirect(url_for('hello')) # 重定向回主页


@app.errorhandler(404) # 传入要处理的错误代码
def page_not_found(e): # 接受异常对象作为参数
    # return render_template('404.html'), 404
    return render_template('404_1.html'), 404

@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """Create user."""
    db.create_all()
    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password) # 设置密码

    else:
        click.echo('Creating user...')
        user = User(username=username, name='Admin')
        user.set_password(password) # 设置密码
        db.session.add(user)

    db.session.commit() # 提交数据库会话
    click.echo('Done.')

@login_manager.user_loader
def load_user(user_id): # 创建用户加载回调函数，接受用户 ID 作为参数
    user = User.query.get(int(user_id)) # 用 ID 作为 User 模型的 主键查询对应的用户
    return user # 返回用户对象

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = User.query.first() # 验证用户名和密码是否一致
        if username == user.username and user.validate_password( password):
            login_user(user) # 登入用户
            flash('Login success.')
            return redirect(url_for('hello')) # 重定向到主页

        flash('Invalid username or password.') # 如果验证失败，显 示错误消息
        return redirect(url_for('login')) # 重定向回登录页面

    return render_template('login.html')

@app.route('/logout')
@login_required # 用于视图保护，后面会详细介绍
def logout():
    logout_user() # 登出用户
    flash('Goodbye.')
    return redirect(url_for('hello')) # 重定向回首页

if __name__ == '__main__':
    app.run()
