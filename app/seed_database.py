from app.database import engine, SessionLocal
from app.models import Base, Action, ActionConfig, RIGAction, RIGActionConfig  # ✅ Import RIGActionConfig

# ✅ Create Tables
def init_db():
    """
    Create tables only once.
    """
    Base.metadata.create_all(engine)

# ✅ Predefined Actions & Configurations
def seed_database():
    """
    Seeds the database with predefined actions and configurations.
    """
    db = SessionLocal()

    # Check if actions already exist (Prevent duplicate insertions)
    if db.query(Action).first() is None:
        actions = [
            Action(id=1, name="Click on Screen", type="click"),
            Action(id=2, name="Type Input", type="type_input"),
            Action(id=3, name="Swipe", type="swipe"),
            Action(id=4, name="Swipe Until", type="swipe_until"),
            Action(id=5, name="Set Time Delay", type="set_time_delay"),
        ]
        db.add_all(actions)
        db.commit()

    # Check if action configs exist
    if db.query(ActionConfig).first() is None:
        configs = [
            ActionConfig(action_id=1, option_name="Click", valid_values={"x": "numeric", "y": "numeric"}),
            ActionConfig(action_id=2, option_name="Type", valid_values={"text": "string"}),
            ActionConfig(action_id=3, option_name="Swipe", valid_values={"direction": ["Up", "Down", "Left", "Right"]}),
            ActionConfig(action_id=4, option_name="Swipe Until", valid_values={
                "direction": ["Up", "Down", "Left", "Right"],
                "type": ["word", "image"],
                "value": "string"
            }),
            ActionConfig(action_id=5, option_name="Time", valid_values={"seconds": "numeric"})
        ]
        db.add_all(configs)
        db.commit()

    # ✅ Populate RIGAction (Fix Missing Entries)
    if db.query(RIGAction).first() is None:
        rig_actions = [
            RIGAction(id=1, name="Switch Phone", type="switch_phone"),
            RIGAction(id=2, name="Set Time Delay", type="set_time_delay"),
            RIGAction(id=3, name="Add Workflow", type="add_workflow"),
        ]
        db.add_all(rig_actions)
        db.commit()

    # ✅ Populate RIGActionConfig (Fix Missing Configs)
    if db.query(RIGActionConfig).first() is None:
        rig_action_configs = [
            RIGActionConfig(rig_action_id=1, option_name="Phone", valid_values={"phone_id": "numeric"}),
            RIGActionConfig(rig_action_id=2, option_name="Time", valid_values={"seconds": "numeric"}),
            RIGActionConfig(rig_action_id=3, option_name="Workflow", valid_values={"workflow_id": "numeric"}),
        ]
        db.add_all(rig_action_configs)
        db.commit()

    db.close()
    print("✅ Database Seeding Completed!")

# ✅ Initialize Database and Seed Data
if __name__ == "__main__":
    init_db()  # Create tables
    seed_database()  # Insert predefined data
