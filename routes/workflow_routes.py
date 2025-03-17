from flask import Blueprint, request, jsonify
from app.database import SessionLocal
from app.models import Workflow, WorkflowSteps, Action, WeekdayEnum
from sqlalchemy.orm import joinedload

workflow_routes = Blueprint("workflow_routes", __name__)
db = SessionLocal()

# 🔹 Mapping Full Weekday Names to Enum Values
DAY_MAPPING = {
    "Monday": WeekdayEnum.MO.value,
    "Tuesday": WeekdayEnum.TU.value,
    "Wednesday": WeekdayEnum.WE.value,
    "Thursday": WeekdayEnum.TH.value,
    "Friday": WeekdayEnum.FR.value,
    "Saturday": WeekdayEnum.SA.value,
    "Sunday": WeekdayEnum.SU.value
}

# 🔹 Create a New Workflow
@workflow_routes.route("/workflows", methods=["POST"])
def create_workflow():
    data = request.json

    start_day_enum = DAY_MAPPING.get(data["start_day"])
    end_day_enum = DAY_MAPPING.get(data["end_day"])

    if not start_day_enum or not end_day_enum:
        return jsonify({"error": "Invalid start_day or end_day. Use Monday-Sunday."}), 400

    new_workflow = Workflow(
        name=data["name"],
        start_hour=data["start_hour"],
        end_hour=data["end_hour"],
        start_day=start_day_enum,
        end_day=end_day_enum
    )
    db.add(new_workflow)
    db.commit()
    return jsonify({"message": "Workflow created", "id": new_workflow.id}), 201

# 🔹 Get All Workflows
@workflow_routes.route("/workflows", methods=["GET"])
def get_workflows():
    workflows = db.query(Workflow).all()
    return jsonify([{"id": w.id, "name": w.name} for w in workflows])

# 🔹 Add a Step to a Workflow
@workflow_routes.route("/workflows/<int:workflow_id>/steps", methods=["POST"])
def add_workflow_step(workflow_id):
    data = request.json

    new_step = WorkflowSteps(
        workflow_id=workflow_id,
        action_id=data["action_id"],
        selected_value=data["selected_value"],  # ✅ JSON structure is now consistent!
        step_order=data["step_order"]
    )
    db.add(new_step)
    db.commit()
    return jsonify({"message": "Step added", "step_id": new_step.id}), 201

# 🔹 Get All Steps in a Workflow
@workflow_routes.route("/workflows/<int:workflow_id>/steps", methods=["GET"])
def get_workflow_steps(workflow_id):
    steps = db.query(WorkflowSteps).filter_by(workflow_id=workflow_id).order_by(WorkflowSteps.step_order).all()
    return jsonify([
        {
            "step_id": s.id,  # ✅ Added step_id to the response
            "step_order": s.step_order,
            "action": db.query(Action).filter_by(id=s.action_id).first().name,
            "selected_value": s.selected_value
        } for s in steps
    ])

# 🔹 Move Workflow Step Up
@workflow_routes.route("/workflows/<int:workflow_id>/steps/<int:step_id>/move_up", methods=["PUT"])
def move_workflow_step_up(workflow_id, step_id):
    step = db.query(WorkflowSteps).filter_by(id=step_id, workflow_id=workflow_id).first()
    if not step:
        return jsonify({"message": "Step not found"}), 404

    prev_step = db.query(WorkflowSteps).filter(
        WorkflowSteps.workflow_id == workflow_id, 
        WorkflowSteps.step_order < step.step_order
    ).order_by(WorkflowSteps.step_order.desc()).first()

    if not prev_step:
        return jsonify({"message": "Step is already at the top"}), 400

    step.step_order, prev_step.step_order = prev_step.step_order, step.step_order
    db.commit()
    
    return jsonify({"message": "Step moved up"}), 200

# 🔹 Move Workflow Step Down
@workflow_routes.route("/workflows/<int:workflow_id>/steps/<int:step_id>/move_down", methods=["PUT"])
def move_workflow_step_down(workflow_id, step_id):
    step = db.query(WorkflowSteps).filter_by(id=step_id, workflow_id=workflow_id).first()
    if not step:
        return jsonify({"message": "Step not found"}), 404

    next_step = db.query(WorkflowSteps).filter(
        WorkflowSteps.workflow_id == workflow_id, 
        WorkflowSteps.step_order > step.step_order
    ).order_by(WorkflowSteps.step_order.asc()).first()

    if not next_step:
        return jsonify({"message": "Step is already at the bottom"}), 400

    step.step_order, next_step.step_order = next_step.step_order, step.step_order
    db.commit()
    
    return jsonify({"message": "Step moved down"}), 200

# 🔹 Delete a Workflow
@workflow_routes.route("/workflows/<int:workflow_id>", methods=["DELETE"])
def delete_workflow(workflow_id):
    workflow = db.query(Workflow).filter_by(id=workflow_id).first()
    if not workflow:
        return jsonify({"message": "Workflow not found"}), 404
    db.delete(workflow)
    db.commit()
    return jsonify({"message": "Workflow deleted"}), 200

# Get a single workflow by ID
@workflow_routes.route("/workflows/<int:workflow_id>", methods=["GET"])
def get_workflow(workflow_id):
    workflow = db.query(Workflow).filter_by(id=workflow_id).first()
    
    if not workflow:
        return jsonify({"error": "Workflow not found"}), 404
    
    return jsonify({
        "id": workflow.id,
        "name": workflow.name,
        "start_hour": workflow.start_hour,
        "end_hour": workflow.end_hour,
        "start_day": workflow.start_day.value,  # Convert enum to string
        "end_day": workflow.end_day.value  # Convert enum to string
    })
