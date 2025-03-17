from flask import Blueprint
from routes.workflow_routes import workflow_routes
from routes.rig_routes import rig_routes
from routes.action_routes import action_routes
from routes.phone_routes import phone_routes
from routes.rig_action_routes import rig_action_routes

# Create the main Blueprint
routes = Blueprint("routes", __name__)

# Register all route blueprints
routes.register_blueprint(workflow_routes, url_prefix="")
routes.register_blueprint(rig_routes, url_prefix="")
routes.register_blueprint(action_routes, url_prefix="")
routes.register_blueprint(phone_routes, url_prefix="")
routes.register_blueprint(rig_action_routes, url_prefix="")
