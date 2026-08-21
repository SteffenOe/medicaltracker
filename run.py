import os
from app import create_app, db
from config import BASE_DIR

app = create_app()

if __name__ == '__main__':
    # Ordner 'database/' sicherstellen
    os.makedirs(os.path.join(BASE_DIR, 'database'), exist_ok=True)
    
    with app.app_context():
        db.create_all()
        print("Datenbanktabellen in 'database/medical_tracker.db' erfolgreich erzeugt.")
        
    app.run(debug=True, port=5000)