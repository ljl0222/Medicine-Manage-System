from db_manage.db import db

class User(db.Model):
    __tablename__ = 'User'
    ## 主键
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    isAdmin = db.Column(db.Integer)