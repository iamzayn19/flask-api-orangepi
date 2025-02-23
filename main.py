from sqlalchemy.orm import Session
from app.database import engine, Base, SessionLocal
from app.models import Action, RIGAction, ActionConfig, RIGActionConfig

def insert_defaults():
    db: Session = SessionLocal()

    default_actions = [
        {"name": "Click on Screen", "type": "click"},
        {"name": "Type Input", "type": "type_input"},
        {"name": "Swipe on Screen", "type": "swipe"},
        {"name": "Set Time Delay", "type": "set_time_delay"},
    ]
    
    action_map = {}
    for action in default_actions:
        existing_action = db.query(Action).filter(Action.type == action["type"]).first()
        if not existing_action:
            new_action = Action(name=action["name"], type=action["type"])
            db.add(new_action)
            db.flush()
            action_map[action["type"]] = new_action.id
        else:
            action_map[action["type"]] = existing_action.id

    default_action_configs = [
        {"action_id": action_map["swipe"], "option_name": "direction", "valid_values": {"values": ["up", "down", "left", "right"]}},
        {"action_id": action_map["set_time_delay"], "option_name": "duration", "valid_values": {"values": ["seconds"]}},
                {"action_id": action_map["click"], "option_name": "x", "valid_values": {"values": ["0-1000"]}},
        {"action_id": action_map["click"], "option_name": "y", "valid_values": {"values": ["0-1000"]}},
        {"action_id": action_map["type_input"], "option_name": "input_text", "valid_values": {"values": ["text"]}}
    ]

    for config in default_action_configs:
        existing_config = db.query(ActionConfig).filter(ActionConfig.action_id == config["action_id"]).first()
        if not existing_config:
            db.add(ActionConfig(action_id=config["action_id"], option_name=config["option_name"], valid_values=config["valid_values"]))

    db.commit()
    db.close()

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    insert_defaults()
    print("Database setup complete with default actions and configurations.")
