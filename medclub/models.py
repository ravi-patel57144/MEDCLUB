from medclub import db
from datetime import datetime

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    fname=db.Column(db.String(20),nullable=False)
    lname = db.Column(db.String(20),nullable=False)
    email=db.Column(db.String(80),unique=True,nullable=False)
    mobile=db.Column(db.String(10),unique=True,nullable=False)
    address=db.Column(db.String(500),nullable=False)
    password=db.Column(db.String(100),nullable=False)
    is_verified=db.Column(db.Boolean,default=False,nullable=False)
    rejected= db.Column(db.Boolean, nullable=False, default=False)
    blocked=db.Column(db.Boolean, nullable=False,default=False)
    # medicine_doner=db.relationship('Donate',backref='doner_user',lazy=True)
    # medicine_requester = db.relationship('Request', backref='requester_user',lazy=True)

    def __repr__(self):
        return f"{self.fname} {self.lname} {self.email}"

class Ngo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    ngo_name=db.Column(db.String(20),unique=True,nullable=False)
    owner_name = db.Column(db.String(20), unique=True,nullable=False)
    email=db.Column(db.String(80),unique=True,nullable=False)
    mobile=db.Column(db.String(10),unique=True,nullable=False)
    address=db.Column(db.String(500),nullable=False)
    password=db.Column(db.String(100),nullable=False)
    upload_verified_doc=db.Column(db.String(20),nullable=False)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    rejected= db.Column(db.Boolean, nullable=False, default=False)
    blocked=db.Column(db.Boolean, nullable=False,default=False)
    # receiver_ngo = db.relationship('Donate', backref='receiver_ngo', lazy=True)
    # doner_ngo = db.relationship('Request', backref='doner_ngo',lazy=True)

    def __repr__(self):
        return f"{self.ngo_name} {self.owner_name} {self.email}"

class Donate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    medicine_name = db.Column(db.String(20), nullable=False)
    donater_user_id=db.Column(db.Integer)
    receiver_ngo_id=db.Column(db.Integer)
    donation_date=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    quantity=db.Column(db.Integer,nullable=False)
    medicine_img = db.Column(db.String(20), nullable=False)
    accepted=db.Column(db.Boolean,nullable=False,default=False)
    rejected=db.Column(db.Boolean,nullable=False,default=False)
    rejected_by=db.Column(db.Integer,nullable=True)
    comment=db.Column(db.String(150),nullable=True)
    expiry_date=db.Column(db.String(150),nullable=False)
    delivered = db.Column(db.Boolean, nullable=False, default=False)


class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    medicine_name = db.Column(db.String(20), nullable=False)
    requester_user_id=db.Column(db.Integer)
    donater_ngo_id=db.Column(db.Integer)
    request_date=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    quantity=db.Column(db.Integer,nullable=False)
    prescription = db.Column(db.String(20), nullable=False)
    doctor_name = db.Column(db.String(20), nullable=False)
    accepted=db.Column(db.Boolean,nullable=False,default=False)
    rejected = db.Column(db.Boolean, nullable=False, default=False)
    rejected_by = db.Column(db.Integer,nullable=True)
    comment = db.Column(db.String(150), nullable=True)
    delivered=db.Column(db.Boolean,nullable=False,default=False)

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    medicine_name = db.Column(db.String(20), nullable=False)
    ngo_id=db.Column(db.Integer,nullable=False)
    quantity=db.Column(db.Integer,nullable=False)
    ngo_name=db.Column(db.String(100),nullable=False)


class Admin(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(100),unique=True)
    password=db.Column(db.String(100))



