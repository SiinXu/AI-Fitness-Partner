from . import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.types import TypeDecorator, TEXT
import json
from werkzeug.security import generate_password_hash, check_password_hash

class JSONType(TypeDecorator):
    impl = TEXT

    def process_bind_param(self, value, dialect):
        if value is not None:
            return json.dumps(value)
        return None

    def process_result_value(self, value, dialect):
        if value is not None:
            return json.loads(value)
        return None

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    fitness_level = db.Column(db.String(50), default='beginner')
    fitness_goals = db.Column(JSONType, nullable=True)
    modelscope_api_key = db.Column(db.String(200), nullable=True)
    fish_audio_api_key = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    workouts = db.relationship('Workout', backref='user', lazy=True)

    def __init__(self, username, email, password, fitness_level=None, fitness_goals=None):
        self.username = username
        self.email = email
        self.set_password(password)
        self.fitness_level = fitness_level
        self.fitness_goals = fitness_goals or {}

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'fitness_level': self.fitness_level,
            'fitness_goals': self.fitness_goals,
            'has_modelscope_key': bool(self.modelscope_api_key),
            'has_fish_audio_key': bool(self.fish_audio_api_key),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
