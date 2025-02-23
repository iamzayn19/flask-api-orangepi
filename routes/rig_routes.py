from flask import Blueprint, request, jsonify
from app.database import SessionLocal
from app.models import RIG, RIGSteps, RIGAction

rig_routes = Blueprint("rig_routes", __name__)
db = SessionLocal()

# Create a RIG
@rig_routes.route("/rigs", methods=["POST"])
def create_rig():
    data = request.json
    new_rig = RIG(name=data["name"], description=data["description"])
    db.add(new_rig)
    db.commit()
    return jsonify({"message": "RIG created", "id": new_rig.id}), 201

# Get all RIGs
@rig_routes.route("/rigs", methods=["GET"])
def get_rigs():
    rigs = db.query(RIG).all()
    return jsonify([{"id": r.id, "name": r.name} for r in rigs])

# Fetch rig action steps (sequence of actions for a RIG)
@rig_routes.route("/rigs/<int:rig_id>/steps", methods=["GET"])
def get_rig_action_steps(rig_id):
    steps = db.query(RIGSteps).filter_by(rig_id=rig_id).order_by(RIGSteps.step_order).all()
    return jsonify([
        {
            "step_order": s.step_order,
            "action": db.query(RIGAction).filter_by(id=s.rig_action_id).first().name,
            "selected_value": s.selected_value
        } for s in steps
    ])

# Delete a RIG
@rig_routes.route("/rigs/<int:rig_id>", methods=["DELETE"])
def delete_rig(rig_id):
    rig = db.query(RIG).filter_by(id=rig_id).first()
    if not rig:
        return jsonify({"message": "RIG not found"}), 404
    db.delete(rig)
    db.commit()
    return jsonify({"message": "RIG deleted"}), 200

# Move RIG Step UP
@rig_routes.route("/rigs/<int:rig_id>/steps/<int:step_id>/move_up", methods=["PUT"])
def move_rig_step_up(rig_id, step_id):
    step = db.query(RIGSteps).filter_by(id=step_id, rig_id=rig_id).first()
    if not step:
        return jsonify({"message": "Step not found"}), 404

    # Get the previous step (lower order)
    prev_step = db.query(RIGSteps).filter(
        RIGSteps.rig_id == rig_id, 
        RIGSteps.step_order < step.step_order
    ).order_by(RIGSteps.step_order.desc()).first()

    if not prev_step:
        return jsonify({"message": "Step is already at the top"}), 400

    # Swap order values
    step.step_order, prev_step.step_order = prev_step.step_order, step.step_order
    db.commit()
    
    return jsonify({"message": "Step moved up"}), 200

# Move RIG Step DOWN
@rig_routes.route("/rigs/<int:rig_id>/steps/<int:step_id>/move_down", methods=["PUT"])
def move_rig_step_down(rig_id, step_id):
    step = db.query(RIGSteps).filter_by(id=step_id, rig_id=rig_id).first()
    if not step:
        return jsonify({"message": "Step not found"}), 404

    # Get the next step (higher order)
    next_step = db.query(RIGSteps).filter(
        RIGSteps.rig_id == rig_id, 
        RIGSteps.step_order > step.step_order
    ).order_by(RIGSteps.step_order.asc()).first()

    if not next_step:
        return jsonify({"message": "Step is already at the bottom"}), 400

    # Swap order values
    step.step_order, next_step.step_order = next_step.step_order, step.step_order
    db.commit()
    
    return jsonify({"message": "Step moved down"}), 200
