
from flask import Flask
from flask_cors import CORS
from models import db, migrate
from routes_auth import auth_bp
from routes_profile import profile_bp
from routes_emergency import emergency_bp
from routes_qr import qr_bp
from routes_uploads import uploads_bp
import os

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///anerita.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET','supersecret')
    app.config['UPLOAD_DIR'] = os.environ.get('UPLOAD_DIR','uploads')
    os.makedirs(app.config['UPLOAD_DIR'], exist_ok=True)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(profile_bp, url_prefix='/api')
    app.register_blueprint(emergency_bp, url_prefix='/api')
    app.register_blueprint(qr_bp, url_prefix='/api')
    app.register_blueprint(uploads_bp, url_prefix='/api')

    @app.get('/health')
    def health(): return {"ok": True}

    return app

app = create_app()
