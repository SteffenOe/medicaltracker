from flask import Flask
from config import Config
from app.routes.main import main_bp
from app.routes.medikamente import medikamente_bp
from app.routes.patient import patient_bp
from app.routes.vitaldaten import vitaldaten_bp
from app.routes.termine import termine_bp
from app.routes.berichte import berichte_bp

from app.models import db

def create_app(config_class=Config):
    """Instanziierung der Anwendung"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialisierung der Persistenzschicht
    db.init_app(app)

    # Registrierung der funktionalen Domänen-Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(medikamente_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(vitaldaten_bp)
    app.register_blueprint(termine_bp)
    app.register_blueprint(berichte_bp)

    return app