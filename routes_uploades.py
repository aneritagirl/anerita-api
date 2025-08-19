from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Profile, Document
import os, werkzeug

uploads_bp = Blueprint('uploads', __name__)
SAFE_EXT = {'.pdf','.png','.jpg','.jpeg','.webp'}

@uploads_bp.post('/vault/upload')
@jwt_required()
def upload():
    uid = get_jwt_identity()
    p = Profile.query.filter_by(user_id=uid).first()
    if not p: return {"error":"no profile"}, 400
    if 'file' not in request.files: return {"error":"missing file"}, 400
    f = request.files['file']
    ext = os.path.splitext(f.filename)[1].lower()
    if ext not in SAFE_EXT: return {"error":"unsupported file"}, 415
    safe_name = werkzeug.utils.secure_filename(f.filename)
    dest_dir = os.environ.get('UPLOAD_DIR','uploads')
    os.makedirs(dest_dir, exist_ok=True)
    path = os.path.join(dest_dir, safe_name)
    f.save(path)
    d = Document(profile_id=p.id, filename=safe_name, mime=f.mimetype, path=path)
    db.session.add(d); db.session.commit()
    return {"ok": True, "doc_id": d.id, "filename": d.filename}
