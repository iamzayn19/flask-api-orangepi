from flask import Blueprint, request, jsonify
from app.database import SessionLocal
from app.models import RIG, RIGSteps, RIGAction, Phone

rig_routes = Blueprint("rig_routes", __name__)
db = SessionLocal()

# 🔹 Create a RIG
@rig_routes.route("/rigs", methods=["POST"])
def create_rig():
    data = request.json
    new_rig = RIG(name=data["name"], description=data["description"])
    db.add(new_rig)
    db.commit()
    return jsonify({"message": "RIG created", "id": new_rig.id}), 201

# 🔹 Get All RIGs
@rig_routes.route("/rigs", methods=["GET"])
def get_rigs():
    rigs = db.query(RIG).all()
    return jsonify([{"id": r.id, "name": r.name} for r in rigs])

# 🔹 Assign a Step to a RIG
@rig_routes.route("/rigs/<int:rig_id>/steps", methods=["POST"])
def add_rig_step(rig_id):
    data = request.json
    new_step = RIGSteps(
        rig_id=rig_id,
        rig_action_id=data["rig_action_id"],
        selected_value=data["selected_value"],
        step_order=data["step_order"]
    )
    db.add(new_step)
    db.commit()
    return jsonify({"message": "Step added to RIG", "step_id": new_step.id}), 201

# 🔹 Get RIG Steps
@rig_routes.route("/rigs/<int:rig_id>/steps", methods=["GET"])
def get_rig_steps(rig_id):
    steps = db.query(RIGSteps).filter_by(rig_id=rig_id).order_by(RIGSteps.step_order).all()
    return jsonify([
        {
            "step_id": s.id,
            "step_order": s.step_order,
            "action": db.query(RIGAction).filter_by(id=s.rig_action_id).first().name,
            "selected_value": s.selected_value
        } for s in steps
    ])

# 🔹 Remove a Step from RIG
@rig_routes.route("/rigs/<int:rig_id>/steps/<int:step_id>", methods=["DELETE"])
def remove_rig_step(rig_id, step_id):
    step = db.query(RIGSteps).filter_by(id=step_id, rig_id=rig_id).first()
    
    if not step:
        return jsonify({"message": "Step not found"}), 404
    
    db.delete(step)
    db.commit()
    
    return jsonify({"message": "Step removed successfully"}), 200

# 🔹 Move RIG Step Up
@rig_routes.route("/rigs/<int:rig_id>/steps/<int:step_id>/move_up", methods=["PUT"])
def move_rig_step_up(rig_id, step_id):
    step = db.query(RIGSteps).filter_by(id=step_id, rig_id=rig_id).first()
    
    if not step:
        return jsonify({"message": "Step not found"}), 404

    prev_step = db.query(RIGSteps).filter(
        RIGSteps.rig_id == rig_id, 
        RIGSteps.step_order < step.step_order
    ).order_by(RIGSteps.step_order.desc()).first()

    if not prev_step:
        return jsonify({"message": "Step is already at the top"}), 400

    step.step_order, prev_step.step_order = prev_step.step_order, step.step_order
    db.commit()

    return jsonify({"message": "Step moved up"}), 200

# 🔹 Move RIG Step Down
@rig_routes.route("/rigs/<int:rig_id>/steps/<int:step_id>/move_down", methods=["PUT"])
def move_rig_step_down(rig_id, step_id):
    step = db.query(RIGSteps).filter_by(id=step_id, rig_id=rig_id).first()
    
    if not step:
        return jsonify({"message": "Step not found"}), 404

    next_step = db.query(RIGSteps).filter(
        RIGSteps.rig_id == rig_id, 
        RIGSteps.step_order > step.step_order
    ).order_by(RIGSteps.step_order.asc()).first()

    if not next_step:
        return jsonify({"message": "Step is already at the bottom"}), 400

    step.step_order, next_step.step_order = next_step.step_order, step.step_order
    db.commit()
    
    return jsonify({"message": "Step moved down"}), 200

# 🔹 Delete a RIG
@rig_routes.route("/rigs/<int:rig_id>", methods=["DELETE"])
def delete_rig(rig_id):
    rig = db.query(RIG).filter_by(id=rig_id).first()
    if not rig:
        return jsonify({"message": "RIG not found"}), 404
    db.delete(rig)
    db.commit()
    return jsonify({"message": "RIG deleted"}), 200

# 🔹 Get a single RIG by ID
@rig_routes.route("/rigs/<int:rig_id>", methods=["GET"])
def get_rig(rig_id):
    rig = db.query(RIG).filter_by(id=rig_id).first()
    if not rig:
        return jsonify({"error": "RIG not found"}), 404
    
    # Fetch phones assigned to this RIG
    phones = db.query(Phone).filter_by(rig_id=rig_id).all()
    phone_list = [{"id": p.id, "serial_number": p.serial_number} for p in phones]

    return jsonify({
        "id": rig.id,
        "name": rig.name,
        "description": rig.description,
        "phones": phone_list
    })
