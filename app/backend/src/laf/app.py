from flask import Flask, jsonify, request
from flask_cors import CORS
from .models import db, Workflow, Task, Result
from .tasks import run_instrument_task


def create_app():
    app = Flask(__name__)
    app.config.from_object("laf.config.Config")
    CORS(app)

    db.init_app(app)

    @app.route("/api/workflows", methods=["POST"])
    def create_workflow():
        data = request.get_json()
        new_workflow = Workflow()
        new_workflow.name = data["name"]
        db.session.add(new_workflow)
        db.session.commit()

        for task_data in data.get("tasks", []):
            new_task = Task()
            new_task.name = task_data["name"]
            new_task.instrument = task_data["instrument"]
            new_task.workflow_id = new_workflow.id
            db.session.add(new_task)
        db.session.commit()

        # Start the first task
        first_task = (
            Task.query.filter_by(workflow_id=new_workflow.id).order_by(Task.id).first()
        )
        if first_task:
            run_instrument_task(
                task_id=first_task.id, instrument_name=first_task.instrument
            )

        return jsonify({"id": new_workflow.id, "name": new_workflow.name}), 201

    @app.route("/api/workflows", methods=["GET"])
    def get_workflows():
        workflows = Workflow.query.order_by(Workflow.created_at.desc()).all()
        output = []
        for w in workflows:
            tasks = []
            for t in w.tasks:
                results = [{"id": r.id, "data": r.data} for r in t.results]
                tasks.append(
                    {
                        "id": t.id,
                        "name": t.name,
                        "instrument": t.instrument,
                        "status": t.status,
                        "results": results,
                    }
                )
            output.append({"id": w.id, "name": w.name, "tasks": tasks})
        return jsonify(output)

    @app.route("/api/webhook/task/update", methods=["POST"])
    def webhook_task_update():
        data = request.get_json()
        task = Task.query.get(data["task_id"])
        if not task:
            return jsonify({"error": "Task not found"}), 404

        task.status = data["status"]
        if "results" in data:
            new_result = Result()
            new_result.task_id = task.id
            new_result.data = data["results"]
            db.session.add(new_result)

        db.session.commit()

        # If completed, trigger next task in workflow
        if task.status == "completed":
            tasks_in_workflow = (
                Task.query.filter_by(workflow_id=task.workflow_id)
                .order_by(Task.id)
                .all()
            )
            current_task_index = tasks_in_workflow.index(task)
            if current_task_index + 1 < len(tasks_in_workflow):
                next_task = tasks_in_workflow[current_task_index + 1]
                run_instrument_task.delay(
                    task_id=next_task.id, instrument_name=next_task.instrument
                )

        return jsonify({"message": "Task updated"}), 200

    return app


app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000)
