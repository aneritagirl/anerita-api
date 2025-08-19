from flask import Blueprint, send_file, jsonify
from models import Profile
import qrcode, io

qr_bp = Blueprint('qr', __name__)

@qr_bp.get('/qr/<code>.png')
def qr_png(code):
    # allow previsualization even before auth (public)
    img = qrcode.make(f"https://anerita.com/app.html?code={code}")
    buf = io.BytesIO(); img.save(buf, format='PNG'); buf.seek(0)
    return send_file(buf, mimetype='image/png')

@qr_bp.get('/qr/by-profile/<int:pid>')
def qr_by_profile(pid):
    p = Profile.query.get_or_404(pid)
    return jsonify({"qr_code": p.qr_code, "qr_url": f"https://anerita.com/app.html?code={p.qr_code}", "qr_png": f"/api/qr/{p.qr_code}.png"})
