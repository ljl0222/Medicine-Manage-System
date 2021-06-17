from db_manage.db import db

class Prescription(db.Model):
    __tablename__ = 'Prescription'
    ## 主键
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(50), nullable=False)
    indications = db.Column(db.String(50), nullable=False)
    # 使用了很不聪明的写法，打算将他们直接存成List的关系(不是懒得用关系表)，不同的序号之间用_隔开
    compositionList = db.Column(db.Text)
    effect = db.Column(db.String(50), nullable=False)
    dosage = db.Column(db.String(50), nullable=False)