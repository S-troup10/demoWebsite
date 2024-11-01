from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class Auth:
    def __init__(self, app):
        db.init_app(app)
        with app.app_context():
            db.create_all()

    class User(db.Model):
        __tablename__ = 'users'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(150), unique=True, nullable=False)
        email = db.Column(db.String(150), unique=True, nullable=False)
        password = db.Column(db.String(150), nullable=False)
        entries = db.relationship('Entry', backref='user', lazy=True)

    class Entry(db.Model):
        __tablename__ = 'entries'
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
        entry_date = db.Column(db.DateTime, default=datetime.now())
        entry_text = db.Column(db.Text, nullable=False)

    def add_entry(self, user_id, entry_text, entry_date):
        new_entry = self.Entry(user_id=user_id, entry_text=entry_text, entry_date=entry_date)
        db.session.add(new_entry)
        db.session.commit()

    
    def format_entry_date(entry_date):
       entry_date 
        
    def get_user_entries(self, user_id):
        return [
            {'id': entry.id, 'entry_text': entry.entry_text, 'entry_date': str(entry.entry_date)[:10]}
            for entry in self.Entry.query.filter_by(user_id=user_id).order_by(self.Entry.id.desc()).all()
        ]


    def register_user(self, name, email, password):
        hashed_password = generate_password_hash(password)
        new_user = self.User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

    def validate_login(self, email, password):
        user = self.User.query.filter_by(email=email).first()
        return user if user and check_password_hash(user.password, password) else None

    def isEmailTaken(self, email):
        return bool(self.User.query.filter_by(email=email).first())

    def delete_entry(self, entry_id):
        entry = self.Entry.query.get(entry_id)
        if entry:
            db.session.delete(entry)
            db.session.commit()
