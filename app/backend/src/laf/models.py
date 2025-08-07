from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import event
import datetime

db = SQLAlchemy()


class Workflow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    status = db.Column(
        db.String(64), default="pending"
    )  # pending, running, completed, failed
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    author = db.Column(db.String(128), nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )
    tasks = db.relationship(
        "Task", backref="workflow", lazy=True, cascade="all, delete-orphan"
    )


class StandardTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    type = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text)
    parameter_schema = db.Column(JSONB)
    enabled = db.Column(db.Boolean, default=True)
    created_at = db.Column(
        db.DateTime, default=datetime.datetime.now(datetime.timezone.utc)
    )
    author = db.Column(db.String(128), nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.datetime.now(datetime.timezone.utc),
        onupdate=datetime.datetime.now(datetime.timezone.utc),
    )


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workflow_id = db.Column(db.Integer, db.ForeignKey("workflow.id"), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    instrument = db.Column(db.String(128), nullable=False)  # e.g., 'instrument-a'
    status = db.Column(
        db.String(64), default="pending"
    )  # pending, running, completed, failed
    order_index = db.Column(db.Integer, default=0)  # To maintain task order
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )
    results = db.relationship(
        "Result", backref="task", lazy=True, cascade="all, delete-orphan"
    )


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey("task.id"), nullable=False)
    data = db.Column(JSONB)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
