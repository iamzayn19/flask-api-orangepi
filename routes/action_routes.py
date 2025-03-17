from flask import Blueprint, jsonify
from app.database import SessionLocal
from app.models import Action, ActionConfig

action_routes = Blueprint("action_routes", __name__)
db = SessionLocal()

# 🔹 Get All Actions
@action_routes.route("/actions", methods=["GET"])
def get_actions():
    actions = db.query(Action).all()
    return jsonify([{"id": a.id, "name": a.name, "type": a.type} for a in actions])

# 🔹 Get Action Configurations
@action_routes.route("/actions/<int:action_id>/config", methods=["GET"])
def get_action_config(action_id):
    configs = db.query(ActionConfig).filter_by(action_id=action_id).all()
    return jsonify([
        {"option_name": c.option_name, "valid_values": c.valid_values} for c in configs
    ])
