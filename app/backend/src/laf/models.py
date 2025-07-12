from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB
import datetime

db = SQLAlchemy()

class Workflow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    tasks = db.relationship('Task', backref='workflow', lazy=True, cascade="all, delete-orphan")

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workflow_id = db.Column(db.Integer, db.ForeignKey('workflow.id'), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    instrument = db.Column(db.String(128), nullable=False) # e.g., 'instrument-a'
    status = db.Column(db.String(64), default='pending') # pending, running, completed, failed
    results = db.relationship('Result', backref='task', lazy=True, cascade="all, delete-orphan")

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    data = db.Column(JSONB)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)