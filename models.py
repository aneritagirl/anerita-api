
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import uuid

db = SQLAlchemy()
migrate = Migrate()

def new_code(): return uuid.uuid4().hex[:10]

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True, nullable=False)
    pw_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    profiles = db.relationship('Profile', backref='owner', lazy=True)

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    full_name = db.Column(db.String(200))
    dob = db.Column(db.String(40))
    blood = db.Column(db.String(10))
    allergies = db.Column(db.Text)       # CSV or JSON string
    conditions = db.Column(db.Text)
    meds = db.Column(db.Text)
    organ_donor = db.Column(db.Boolean, default=False)
    ice_phone = db.Column(db.String(64))
    eol_prefs = db.Column(db.Text)       # JSON string with DNR/DNI etc
    qr_code = db.Column(db.String(40), unique=True, default=new_code)  # public code
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)
    filename = db.Column(db.String(255))
    mime = db.Column(db.String(100))
    path = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ScanEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)
    code = db.Column(db.String(40))
    when = db.Column(db.DateTime, default=datetime.utcnow)
    ip = db.Column(db.String(64))
    ua = db.Column(db.String(255))
