from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config



db = SQLAlchemy()

def create_app(config_class=Config):
    """Main"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from app.routes.main import main_bp
    from app.routes.medikamente import medikamente_bp
    from app.routes.patient import patient_bp
    from app.routes.vitaldaten import vitaldaten_bp
    from app.routes.termine import termine_bp
    from app.routes.berichte import berichte_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(medikamente_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(vitaldaten_bp)
    app.register_blueprint(termine_bp)
    app.register_blueprint(berichte_bp)

    return app