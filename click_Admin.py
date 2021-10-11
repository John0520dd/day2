#-*- coding = utf-8 -*-
#@Time : 2021/10/10 13:06
#@Author : 羊来
#@File : click_Admin.py
#@Software: PyCharm
import click
from app import app,User,Movie,db

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

admin()