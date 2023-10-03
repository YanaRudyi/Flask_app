from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()


class Task(db.Model):
    """Represents a task in the database."""
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80), unique=False, nullable=False)
    status = db.Column(db.String(120), unique=False, nullable=False)
    created_on = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_on = db.Column(db.DateTime(timezone=True), onupdate=func.now())


class User(db.Model):
    """Represents a task in the database."""
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    password = db.Column(db.String(80), unique=False, nullable=False)
