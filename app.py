
import uuid
from flask import Flask, request, json, Response
from flask_sqlalchemy import SQLAlchemy

import config

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)


class Movie_User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20))

class Movie(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))

db.drop_all()
db.create_all() # 在数据库中生成数据表

@app.route('/')
def hello_world():
    return 'Loving this world'


if __name__ == '__main__':
    app.run()
