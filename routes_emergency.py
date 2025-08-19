from flask import Blueprint, request
from models import Profile, ScanEvent, db

emergency_bp = Blueprint('emergency', __name__)

@emergency_bp.get('/emergency/<code>')
def emergency_view(code):
    p = Profile.query.filter_by(qr_code=code).first()
    if not p: return {"error":"not found"}, 404
    # log scan (basic)
    ev = ScanEvent(profile_id=p.id, code=code, ip=request.remote_addr, ua=request.headers.get('User-Agent',''))
    db.session.add(ev); db.session.commit()
    # minimal read-only payload
    return {
        "full_name": p.full_name, "dob": p.dob, "blood": p.blood,
        "allergies": p.allergies, "conditions": p.conditions, "meds": p.meds,
        "organ_donor": p.organ_donor, "ice_phone": p.ice_phone, "eol_prefs": p.eol_prefs
    }
