from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from account_manage import account_model
from db_manage.db import db
from account_manage.account_model import User
from medicine_manage.medicine_model import Medicine
from prescription_manage.prescription_model import Prescription
from sqlalchemy import and_, or_
from . import account

import os
import uuid

# 登录检验（用户名、密码验证）
def valid_login(username, password):
    user = User.query.filter(
        and_(User.username == username, User.password == password)
    ).first()
    if user:
        return True
    else:
        return False

# 注册检验（用户名、邮箱验证）
def valid_regist(username, email):
    user = User.query.filter(
        or_(User.username == username, User.email == email)
    ).first()
    if user:
        return False
    else:
        return True

@account.route('/')
def home():
    allMedicine = Medicine.query.filter().all()
    return render_template('home.html', username=session.get('username'), allMedicine=allMedicine)


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
        elif not valid_regist(request.form['username'], request.form['email']):
            flash('该用户名或者邮箱已经被注册！', 'danger')
        else:
            user = User(
                username = request.form['username'],
                password = request.form['password'],
                email = request.form['email'],
                isAdmin = 0,
                isIdentity = False,
                reason = "",
                img = '../static/headImgs/default.jpg'
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

## 5. 个人中心
@account.route('/panel')
def panel():
    username = session.get('username')
    if not username:
        flash("请先登录！", "danger")
        return redirect(url_for('account_app.home'))
    user = User.query.filter(User.username == username).first()
    db.session.commit()
    return render_template('panel.html', user=user)

@account.route('/identity', methods=['POST', 'GET'])
def identity():
    username = session.get('username')
    if not username:
        flash("请先登录！", "danger")
        return redirect(url_for('account_app.home'))
    
    user = User.query.filter(User.username == username).first()
    user.isIdentity = True
    db.session.commit()
    flash("请等待审核！", "success")
    return redirect(url_for('account_app.panel'))

@account.route('/admin/examine', methods=['POST', 'GET'])
@account.route('/admin/examine/<userName>', methods=['POST', 'GET'])
def examine(userName=""):
    curUsername = session.get('username')
    curUser = User.query.filter(User.username == curUsername).first()

    if (curUser.isAdmin == 0):
        flash("请使用管理员用户登录！", "danger")
        return redirect(url_for('account_app.login'))

    if request.method == 'POST':
        user = User.query.filter(User.username == userName).first()
        if user:
            if request.form.get('isPass') == 'no':
                flash("已拒绝通过！", "success")
            elif request.form.get('isPass') == 'yes':
                user.isAdmin = 1
                flash("已通过！", "success")
            user.isIdentity = False
            user.reason = request.form.get('reason')
            db.session.commit()
        return redirect(url_for('account_app.examine'))

    allUsers = User.query.all()
    userList = []
    for u in allUsers:
        if u.isIdentity:
            userList.append(u)

    return render_template('examine.html', List=userList)

@account.route('/chageHead', methods=['POST', 'GET'])
def chageHead():
    username = session.get('username')
    if not username:
        flash("请先登录！", "danger")
        return redirect(url_for('account_app.home'))
    
    if request.method == 'POST':
        user = User.query.filter(User.username==username).first()
        headImg = request.files['headImg']
        if not headImg:
            flash("未上传文件！", "danger")
            return redirect(url_for('account_app.chageHead'))
        else:
            basepath = os.path.dirname(__file__)
            ext = os.path.splitext(headImg.filename)[1]
            newFileName = str(uuid.uuid1()) + ext

            uploadPath = os.path.join(basepath, '../static/headImgs', newFileName)
            headImg.save(uploadPath)

            if user.img and user.img != '../static/headImgs/default.jpg':
                delPath = os.path.join(basepath, '../static', user.img)
                if os.path.exists(delPath):
                    os.remove(delPath)

            user.img = 'headImgs/' + newFileName
            db.session.commit()
            flash("修改成功！", "success")
            return redirect(url_for('account_app.panel'))
    
    return render_template('chageHead.html')

        




