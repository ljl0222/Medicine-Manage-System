# app.py

## 系统
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

## 自定义
from db_manage.db import db
from account_manage.account_view import account
from medicine_manage.medicine_view import medicine
from prescription_manage.prescription_view import prescription

# 这里需要显式调用，不然不能create_all
# 见了个鬼了，这个地方之前的项目，import和create_all()甚至不是由同一个人写的代码，那当时是怎么create出来的
from account_manage.account_model import User 
from medicine_manage.medicine_model import Medicine
from prescription_manage.prescription_model import Prescription

import config


## 实现
app = Flask(__name__)

## 读取配置
app.config.from_object(config.config)

## 初始化
db.init_app(app)

@app.before_first_request
def create_db():
    db.create_all()


app.register_blueprint(account)
app.register_blueprint(medicine)
app.register_blueprint(prescription)

if __name__ == '__main__':
    app.run(debug=True)