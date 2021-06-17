from db_manage.db import db

class Medicine(db.Model):
    __tablename__ = 'Medicine'
    ## 主键
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(50), nullable=False)
    latinName = db.Column(db.String(50), nullable=False)
    distribution = db.Column(db.String(50), nullable=False)
    nature = db.Column(db.String(50), nullable=False)
    function = db.Column(db.String(50), nullable=False)
    img = db.Column(db.String(256), nullable=False)