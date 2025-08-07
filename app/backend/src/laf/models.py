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
    status = db.Column(db.String(64), default="pending")
    order_index = db.Column(db.Integer, default=0)
    executed_at = db.Column(
        db.DateTime, default=datetime.datetime.now(datetime.timezone.utc)
    )
    # Results should mostly be a pointer to data stored in an external system
    # keeping with the idea of data fabric and not duplicating data.
    results = db.relationship(
        "Result", backref="task", lazy=True, cascade="all, delete-orphan"
    )
    # The actual metadata and instructions should be separate, as some
    # will be stored in external systems like ELN or LIMS. In any case,
    # users should be able to create new tasks without this model needing
    # updated. Moreover, the task will be carried out by a Kubernetes
    # Jobs or Celery, so the task model should not be tied to a specific
    # implementation.
    recipe = db.Column(JSONB)  # Stores task parameters and instructions
    recipe_type = db.Column(
        db.String(64)
    )  # Used for filtering/search (e.g. "Biovia Onelab")
    recipe_hash = db.Column(db.String(64), unique=True)  # Hash of task recipe


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey("task.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    data = db.Column(JSONB)
