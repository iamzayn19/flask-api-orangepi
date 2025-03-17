from flask import Blueprint, request, jsonify
from app.database import SessionLocal
from app.models import Phone, RIG
from sqlalchemy.exc import IntegrityError

phone_routes = Blueprint("phone_routes", __name__)
db = SessionLocal()

# 📌 1️⃣ Create a Phone
@phone_routes.route("/phones", methods=["POST"])
def create_phone():
    data = request.json
    if "serial_number" not in data:
        return jsonify({"error": "serial_number is required"}), 400
    
    new_phone = Phone(rig_id="", serial_number=data["serial_number"])
    try:
        db.add(new_phone)
        db.commit()
        return jsonify({"message": "Phone created", "id": new_phone.id}), 201
    except IntegrityError:
        db.rollback()
        return jsonify({"error": "Phone with this serial number already exists"}), 400

# 📌 2️⃣ Get All Phones
@phone_routes.route("/phones", methods=["GET"])
def get_phones():
    phones = db.query(Phone).all()
    return jsonify([{"id": p.id, "rig_id": p.rig_id, "serial_number": p.serial_number} for p in phones])

# 📌 3️⃣ Get Phones for a Specific RIG
@phone_routes.route("/rigs/<int:rig_id>/phones", methods=["GET"])
def get_phones_for_rig(rig_id):
    phones = db.query(Phone).filter_by(rig_id=rig_id).all()
    return jsonify([{"id": p.id, "serial_number": p.serial_number} for p in phones])

# 📌 4️⃣ Assign a Phone to a RIG
@phone_routes.route("/rigs/<int:rig_id>/phones", methods=["POST"])
def assign_phone_to_rig(rig_id):
    data = request.json
    if "phone_id" not in data:
        return jsonify({"error": "phone_id is required"}), 400
    
    phone = db.query(Phone).filter_by(id=data["phone_id"]).first()
    if not phone:
        return jsonify({"error": "Phone not found"}), 404
    
    phone.rig_id = rig_id
    db.commit()
    return jsonify({"message": "Phone assigned to RIG"}), 200

# 📌 5️⃣ Remove a Phone from a RIG
@phone_routes.route("/rigs/<int:rig_id>/phones/<int:phone_id>", methods=["DELETE"])
def remove_phone_from_rig(rig_id, phone_id):
    phone = db.query(Phone).filter_by(id=phone_id, rig_id=rig_id).first()
    if not phone:
        return jsonify({"error": "Phone not found in this RIG"}), 404
    
    phone.rig_id = None  # Unassign phone from RIG
    db.commit()
    return jsonify({"message": "Phone removed from RIG"}), 200

# 📌 6️⃣ Get a Single Phone by ID
@phone_routes.route("/phones/<int:phone_id>", methods=["GET"])
def get_phone(phone_id):
    phone = db.query(Phone).filter_by(id=phone_id).first()
    if not phone:
        return jsonify({"error": "Phone not found"}), 404

    return jsonify({
        "id": phone.id,
        "rig_id": phone.rig_id,
        "serial_number": phone.serial_number
    })
