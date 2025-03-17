from flask import Blueprint, jsonify
from app.database import SessionLocal
from app.models import RIGAction, RIGActionConfig

rig_action_routes = Blueprint("rig_action_routes", __name__)
db = SessionLocal()

# ✅ **Get all RIG Actions**
@rig_action_routes.route("/rig_actions", methods=["GET"])
def get_rig_actions():
    """
    Returns a list of all available RIG Actions.
    """
    actions = db.query(RIGAction).all()
    return jsonify([{"id": a.id, "name": a.name, "type": a.type} for a in actions])

# ✅ Get details of a specific RIG action
@rig_action_routes.route("/rig_actions/<int:rig_action_id>", methods=["GET"])
def get_rig_action(rig_action_id):
    action = db.query(RIGAction).filter_by(id=rig_action_id).first()
    if not action:
        return jsonify({"error": "RIG Action not found"}), 404
    return jsonify({"id": action.id, "name": action.name, "type": action.type})

# ✅ **Get RIG Action Configurations**
@rig_action_routes.route("/rig_actions/<int:rig_action_id>/config", methods=["GET"])
def get_rig_action_config(rig_action_id):
    """
    Returns configuration options for a given RIG Action.
    """
    configs = db.query(RIGActionConfig).filter_by(rig_action_id=rig_action_id).all()
    
    if not configs:
        return jsonify({"message": "No configuration found for this RIG action"}), 404

    return jsonify([
        {"option_name": c.option_name, "valid_values": c.valid_values} for c in configs
    ])
