from flask import Blueprint, request, jsonify
from app.database import SessionLocal
from app.models import Workflow, WorkflowSteps, Action
from sqlalchemy.orm import joinedload

workflow_routes = Blueprint("workflow_routes", __name__)
db = SessionLocal()

# Create Workflow
@workflow_routes.route("/workflows", methods=["POST"])
def create_workflow():
    data = request.json
    new_workflow = Workflow(
        name=data["name"],
        start_hour=data["start_hour"],
        end_hour=data["end_hour"],
        start_day=data["start_day"],
        end_day=data["end_day"]
    )
    db.add(new_workflow)
    db.commit()
    return jsonify({"message": "Workflow created", "id": new_workflow.id}), 201

# Get all Workflows
@workflow_routes.route("/workflows", methods=["GET"])
def get_workflows():
    workflows = db.query(Workflow).all()
    return jsonify([{"id": w.id, "name": w.name} for w in workflows])

# Fetch workflow action steps (sequence of actions for a workflow)
@workflow_routes.route("/workflows/<int:workflow_id>/steps", methods=["GET"])
def get_workflow_action_steps(workflow_id):
    steps = db.query(WorkflowSteps).filter_by(workflow_id=workflow_id).order_by(WorkflowSteps.step_order).all()
    return jsonify([
        {
            "step_order": s.step_order,
            "action": db.query(Action).filter_by(id=s.action_id).first().name,
            "selected_value": s.selected_value
        } for s in steps
    ])

# Delete a Workflow
@workflow_routes.route("/workflows/<int:workflow_id>", methods=["DELETE"])
def delete_workflow(workflow_id):
    workflow = db.query(Workflow).filter_by(id=workflow_id).first()
    if not workflow:
        return jsonify({"message": "Workflow not found"}), 404
    db.delete(workflow)
    db.commit()
    return jsonify({"message": "Workflow deleted"}), 200

# Move Workflow Step UP
@workflow_routes.route("/workflows/<int:workflow_id>/steps/<int:step_id>/move_up", methods=["PUT"])
def move_workflow_step_up(workflow_id, step_id):
    step = db.query(WorkflowSteps).filter_by(id=step_id, workflow_id=workflow_id).first()
    if not step:
        return jsonify({"message": "Step not found"}), 404

    # Get the previous step (lower order)
    prev_step = db.query(WorkflowSteps).filter(
        WorkflowSteps.workflow_id == workflow_id, 
        WorkflowSteps.step_order < step.step_order
    ).order_by(WorkflowSteps.step_order.desc()).first()

    if not prev_step:
        return jsonify({"message": "Step is already at the top"}), 400

    # Swap order values
    step.step_order, prev_step.step_order = prev_step.step_order, step.step_order
    db.commit()
    
    return jsonify({"message": "Step moved up"}), 200


# Move Workflow Step DOWN
@workflow_routes.route("/workflows/<int:workflow_id>/steps/<int:step_id>/move_down", methods=["PUT"])
def move_workflow_step_down(workflow_id, step_id):
    step = db.query(WorkflowSteps).filter_by(id=step_id, workflow_id=workflow_id).first()
    if not step:
        return jsonify({"message": "Step not found"}), 404

    # Get the next step (higher order)
    next_step = db.query(WorkflowSteps).filter(
        WorkflowSteps.workflow_id == workflow_id, 
        WorkflowSteps.step_order > step.step_order
    ).order_by(WorkflowSteps.step_order.asc()).first()

    if not next_step:
        return jsonify({"message": "Step is already at the bottom"}), 400

    # Swap order values
    step.step_order, next_step.step_order = next_step.step_order, step.step_order
    db.commit()
    
    return jsonify({"message": "Step moved down"}), 200
