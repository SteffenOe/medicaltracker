import os
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

load_dotenv(os.path.join(BASE_DIR, '.env'))

class Config:    
    """Konfiguration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-insecure-key-only-for-local-testing'
    
    DB_REL_PATH = os.environ.get('DATABASE_PATH', 'database/medical_tracker.db')
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, DB_REL_PATH)}"