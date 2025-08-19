
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Profile

profile_bp = Blueprint('profile', __name__)

@profile_bp.get('/profile')
@jwt_required()
def get_profile():
    uid = get_jwt_identity()
    p = Profile.query.filter_by(user_id=uid).first()
    if not p: return {"profile": None}
    return _serialize(p)

@profile_bp.post('/profile')
@jwt_required()
def save_profile():
    uid = get_jwt_identity()
    data = request.json or {}
    p = Profile.query.filter_by(user_id=uid).first()
    if not p: p = Profile(user_id=uid)
    # Simple fields (accept strings/booleans)
    for k in ["full_name","dob","blood","allergies","conditions","meds","ice_phone","eol_prefs"]:
        if k in data: setattr(p,k,data[k])
    if "organ_donor" in data: p.organ_donor = bool(data["organ_donor"])
    db.session.add(p); db.session.commit()
    return _serialize(p)

def _serialize(p: Profile):
    return {"profile":{
        "id": p.id, "qr_code": p.qr_code, "full_name": p.full_name, "dob": p.dob,
        "blood": p.blood, "allergies": p.allergies, "conditions": p.conditions,
        "meds": p.meds, "organ_donor": p.organ_donor, "ice_phone": p.ice_phone,
        "eol_prefs": p.eol_prefs
    }}
