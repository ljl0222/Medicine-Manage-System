from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from db_manage.db import db
from account_manage.account_model import User
from medicine_manage.medicine_model import Medicine
from prescription_manage.prescription_model import Prescription
from sqlalchemy import and_, or_
from . import medicine

import os
import uuid

@medicine.route('/addMedicine', methods=['GET', 'POST'])
def addMedicine():
    username = session.get('username')
    if not username:
        flash("请先登录！", "danger")
        return redirect(url_for('account_app.home'))
    
    if request.method == 'POST':
        img = request.files.get('img')
        if not img:
            flash('未上传图片！', 'danger')
            return render_template('addMedicine.html', username=username)
        img.filename = img.filename.lower()
        basePath = os.path.dirname(__file__)
        ext = os.path.splitext(img.filename)[1]
        newFilename = str(uuid.uuid1()) + ext
        uploadPath = os.path.join(basePath, '../static/medicineImgs', newFilename)
        img.save(uploadPath)

        medicine = Medicine(
            name = request.form.get('name'),
            latinName = request.form.get('latinName'),
            distribution = request.form.get('distribution'),
            nature = request.form.get('nature'),
            function = request.form.get('function'),
            img = 'medicineImgs/' + newFilename
        )
        db.session.add(medicine)
        db.session.commit()
        flash("药品添加成功！", "success")
        return redirect(url_for('account_app.home'))
    return render_template('addMedicine.html', username=username)

@medicine.route('/showMedicine')
@medicine.route('/showMedicine/<medId>')
def showMedicine(medId):
    med = Medicine.query.filter_by(id=medId).first()
    username = session.get('username')
    return render_template('showMedicine.html', medicine=med, username=username)

@medicine.route('/listMedicine')
def listMedicine():
    username = session.get('username')
    if not username:
        flash("请先登录！", "danger")
        return redirect(url_for('account_app.home'))

    List = Medicine.query.filter().all()
    return render_template('listMedicine.html', username=username, List=List)

@medicine.route('/searchMedicine', methods=['GET', 'POST'])
def searchMedicine():
    username = session.get('username')
    if not username:
        flash("请先登录！", "danger")
        return redirect(url_for('account_app.home'))

    keyword = request.form.get('keyword')
    keywordList = keyword.split()

    medSearch = set()
    for key in keywordList:
        medList = Medicine.query.filter(Medicine.name.like("%"+key+"%")).all()
        for med in medList:
            medSearch.add(med)

    List = list(medSearch)

    return render_template('listMedicine.html', username=username, List=List)
