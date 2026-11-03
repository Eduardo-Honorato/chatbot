from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)

_ensure_db_called = False

def ensure_db(app):
    global _ensure_db_called
    if not _ensure_db_called:
        _ensure_db_called = True
        with app.app_context():
            db.create_all()