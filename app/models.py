from sqlalchemy import Column, Integer, String, Enum, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base

class Workflow(Base):
    __tablename__ = "workflows"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    start_hour = Column(Integer, nullable=False)
    end_hour = Column(Integer, nullable=False)
    start_day = Column(Enum('MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU'), nullable=False)
    end_day = Column(Enum('MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU'), nullable=False)

class Action(Base):
    __tablename__ = "actions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    type = Column(Enum('click', 'type_input', 'swipe', 'set_time_delay'), nullable=False)

class ActionConfig(Base):
    __tablename__ = "action_configs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    action_id = Column(Integer, ForeignKey('actions.id'))
    option_name = Column(String(100), nullable=False)
    valid_values = Column(JSON, nullable=False)

class WorkflowSteps(Base):
    __tablename__ = "workflow_steps"
    id = Column(Integer, primary_key=True, autoincrement=True)
    workflow_id = Column(Integer, ForeignKey('workflows.id'))
    action_id = Column(Integer, ForeignKey('actions.id'))
    selected_value = Column(String(100))
    step_order = Column(Integer, nullable=False)

class RIG(Base):
    __tablename__ = "rigs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))

class Phone(Base):
    __tablename__ = "phones"
    id = Column(Integer, primary_key=True, autoincrement=True)
    rig_id = Column(Integer, ForeignKey('rigs.id'))
    serial_number = Column(String(50), unique=True, nullable=False)

class RIGAction(Base):
    __tablename__ = "rig_actions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    type = Column(Enum('switch_phone', 'set_time_delay', 'add_workflow'), nullable=False)

class RIGActionConfig(Base):
    __tablename__ = "rig_action_configs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    rig_action_id = Column(Integer, ForeignKey('rig_actions.id'))
    option_name = Column(String(100), nullable=False)
    valid_values = Column(JSON, nullable=False)

class RIGSteps(Base):
    __tablename__ = "rig_steps"
    id = Column(Integer, primary_key=True, autoincrement=True)
    rig_id = Column(Integer, ForeignKey('rigs.id'))
    rig_action_id = Column(Integer, ForeignKey('rig_actions.id'))
    selected_value = Column(String(100))
    step_order = Column(Integer, nullable=False)
