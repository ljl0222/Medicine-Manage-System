from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from db_manage.db import db
from account_manage.account_model import User
from medicine_manage.medicine_model import Medicine
from prescription_manage.prescription_model import Prescription
from sqlalchemy import and_, or_
from . import prescription

@prescription.route('/addPrescription', methods=['GET', 'POST'])
def addPrescription():
    username = session.get('username')
    if not username:
        flash("请先登录！", "danger")
        return redirect(url_for('account_app.home'))
    
    List = []
    allMedicine = Medicine.query.filter().all()
    for med in allMedicine:
        List.append(med)

    if request.method == 'POST':
        medicineList = request.form.getlist("medicineList")
        # 针对每个元素，对 tempCompositionList 赋值
        # 最终得到的值就是整个组成药材串
        tempCompositionList = ""
        for medicineId in medicineList:
            tempCompositionList = tempCompositionList + '_' + medicineId

        prescription = Prescription(
            name = request.form.get('name'),
            indications = request.form.get('indications'),
            compositionList = tempCompositionList,
            effect = request.form.get('effect'),
            dosage = request.form.get('dosage')
        )
        db.session.add(prescription)
        db.session.commit()
        flash("药方添加成功！", "success")
        return redirect(url_for('account_app.home'))
    return render_template('addPrescription.html', username=username, List=List)


@prescription.route('/search', methods=['GET', 'POST'])
def search():
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

    return render_template('addPrescription.html', username=username, List=List)

@prescription.route('/listPrescription')
def listPrescription():
    username = session.get('username')
    if not username:
        flash("请先登录！", "danger")
        return redirect(url_for('account_app.home'))

    List = Prescription.query.filter().all()

    for i in List:
        idString = i.compositionList.split('_')
        medString = ""
        
        for _id in idString:
            if not _id:
                continue
            med = Medicine.query.filter(Medicine.id==_id).first()
            medString += med.name
            if _id != idString[len(idString) - 1]:
                medString += ','
        i.compositionList = medString

    return render_template('listPrescription.html', username=username, List=List)
