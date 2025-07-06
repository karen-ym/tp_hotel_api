from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from src.models.reserva import Reserva
from src.schemas.reserva_schema import ReservaSchema
from dependencias import db
from src.security.security import token_required

reservas_bp = Blueprint("reservas_bp", __name__)

#Endpoint1: alta de reserva por rango de fechas (Cliente)
@reservas_bp.route("/reservas", methods=["POST"])
@token_required("Cliente")
def crear_reserva(current_user):
    data = request.get_json()
    habitacion_id = data["habitacion_id"]
    inicio = datetime.strptime(data["inicio"], "%Y-%m-%d")
    fin = datetime.strptime(data["fin"], "%Y-%m-%d")

    if fin < inicio:
        return jsonify({"error": "La fecha de fin no puede ser anterior a la de inicio"}), 400

    for i in range((fin - inicio).days + 1):
        fecha = inicio + timedelta(days=i)
        if Reserva.query.filter_by(habitacion_id=habitacion_id, fecha=fecha).first():
            return jsonify({"error": f"La habitación ya está reservada el {fecha.date()}"}), 400

    for i in range((fin - inicio).days + 1):
        fecha = inicio + timedelta(days=i)
        reserva = Reserva(
            habitacion_id=habitacion_id,
            usuario_id=current_user["id"],
            fecha=fecha
        )
        db.session.add(reserva)

    db.session.commit()
    return jsonify({"mensaje": "Reserva realizada con éxito"}), 201

#Endpoint 2: listado de todas las reservas (Empleado)
@reservas_bp.route("/reservas", methods=["GET"])
@token_required("Empleado")
def listar_reservas(current_user):
    reservas = Reserva.query.all()
    schema = ReservaSchema(many=True)
    return jsonify(schema.dump(reservas)), 200