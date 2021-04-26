from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from db_manage.db import db
from account_manage.account_model import User
from sqlalchemy import and_, or_
from . import account

# 登录检验（用户名、密码验证）
def valid_login(username, password):
    user = User.query.filter(
        and_(User.username == username, User.password == password)).first()
    if user:
        return True
    else:
        return False

@account.route('/')
def home():
    return render_template('home.html',
                            username=session.get('username'))


## 测试使用，这里后面改了
@account.route('/list')
def list():
    sql_str = 'select * from User'
    res = db.session.execute(sql_str)
    listUser = res.fetchall()
    return render_template('list.html', listUser=listUser)

## 1. 注册
@account.route('/regist', methods=['GET', 'POST'])
def regist():
    if request.method == 'POST':
        if request.form['password'] != request.form['password_re']:
            flash('两次密码不相同！', 'danger')
        else:
            user = User(
                username = request.form['username'],
                password = request.form['password'],
                email = request.form['email']
            )
            db.session.add(user)
            db.session.commit()
            flash('注册成功！', 'success')
            return redirect(url_for('account_app.home'))
    
    return render_template('regist.html')

## 2. 登录
@account.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        Username = request.form['username']
        Password = request.form['password']
        if valid_login(Username, Password):
            flash("成功登录！",'success')
            session['username'] = request.form.get('username')
            return redirect(url_for('account_app.home'))
        else:
            flash("错误的用户名和密码！",'danger')

    return render_template('login.html')

## 3. 注销
@account.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('account_app.home'))

## 4. 修改密码
@account.route('/changePassword', methods=['GET', 'POST'])
def changePassword():
    if request.method == 'POST':
        username = session.get('username')
        user = User.query.filter(User.username == username).first()
        if user.password == request.form['oldPassword']:
            if request.form['newPassword'] == request.form['newPassword_re']:
                user.password = request.form['newPassword']
                db.session.commit()
                flash("修改成功！", 'success')
                return redirect(url_for('account_app.login'))
            else:
                flash("两次输入的密码不同！", 'warning')
        else:
            flash("原密码错误", 'danger')
    
    return render_template('changePassword.html', 
                            username=session.get('username'))


