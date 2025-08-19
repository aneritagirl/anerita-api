
from flask import Blueprint, request
from models import db, User
from passlib.hash import bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os

jwt = JWTManager()

auth_bp = Blueprint('auth', __name__)
jwt.init_app = lambda app: JWTManager(app)  # helper

@auth_bp.record
def record(setup_state):
    app = setup_state.app
    jwt.init_app(app)

@auth_bp.post('/signup')
def signup():
    data = request.json or {}
    email, pw = data.get('email','').strip().lower(), data.get('password','')
    if not email or not pw: return {"error":"email and password required"}, 400
    if User.query.filter_by(email=email).first(): return {"error":"email in use"}, 409
    u = User(email=email, pw_hash=bcrypt.hash(pw))
    db.session.add(u); db.session.commit()
    token = create_access_token(identity=u.id)
    return {"token": token, "user": {"id": u.id, "email": u.email}}

@auth_bp.post('/login')
def login():
    data = request.json or {}
    email, pw = data.get('email','').strip().lower(), data.get('password','')
    u = User.query.filter_by(email=email).first()
    if not u or not bcrypt.verify(pw, u.pw_hash): return {"error":"invalid credentials"}, 401
    token = create_access_token(identity=u.id)
    return {"token": token, "user": {"id": u.id, "email": u.email}}

@auth_bp.get('/me')
@jwt_required()
def me():
    uid = get_jwt_identity()
    u = User.query.get(uid)
    return {"id": u.id, "email": u.email}
