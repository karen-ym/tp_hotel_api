from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from src.models.habitacion import Habitacion
from src.models.reserva import Reserva
from src.schemas.habitacion_schema import HabitacionSchema
from src.security.security import token_required

busqueda_bp = Blueprint("busqueda_bp", __name__)

#Endpoint: buscar habitaciones con precio menor al valor dado (Cliente)
@busqueda_bp.route("/habitaciones/filtrar", methods=["GET"])
@token_required("cliente")
def buscar_por_precio(current_user):
    try:
        limite = float(request.args.get("precio"))
    except (TypeError, ValueError):
        return jsonify({"mensaje": "Parámetro 'precio' inválido"}), 400

    habitaciones = Habitacion.query.filter(Habitacion.precio <= limite, Habitacion.activa == True).all()
    schema = HabitacionSchema(many=True)
    return jsonify(schema.dump(habitaciones)), 200

#Endpoint2: ver estado de todas las habitaciones en una fecha (Empleado)
@busqueda_bp.route("/habitaciones/diario", methods=["GET"])
@token_required("empleado")
def estado_dia(current_user):
    fecha_str = request.args.get("fecha")
    if not fecha_str:
        return jsonify({"mensaje": "El parámetro 'fecha' es requerido"}), 400

    try:
        fecha = datetime.strptime(fecha_str, "%d/%m/%Y").date()
    except (TypeError, ValueError):
        return jsonify({"mensaje": "Formato de fecha inválido. Usar DD/MM/YYYY"}), 400

    habitaciones = Habitacion.query.filter_by(activa=True).all()
    resultados = []

    for h in habitaciones:
        reservada = Reserva.query.filter(
            Reserva.habitacion_id == h.id,
            Reserva.inicio <= fecha,
            Reserva.fin >= fecha
        ).first() is not None

        resultados.append({
            "numero": h.numero,
            "estado": "ocupada" if reservada else "disponible"
        })

    return jsonify({
        "cantidad": len(habitaciones),
        "habitaciones": resultados
    }), 200

#Endpoint3: buscar habitaciones disponibles en un rango de fechas (Cliente)
@busqueda_bp.route("/habitaciones/disponibles", methods=["GET"])
@token_required("cliente")
def disponibles_rango(current_user):
    try:
        inicio = datetime.strptime(request.args.get("inicio"), "%d/%m/%Y")
        fin = datetime.strptime(request.args.get("fin"), "%d/%m/%Y")

    except (TypeError, ValueError):
        return jsonify({"mensaje": "Fechas inválidas"}), 400

    if fin < inicio:
        return jsonify({"mensaje": "La fecha de fin no puede ser anterior a la de inicio"}), 400

    habitaciones = Habitacion.query.filter_by(activa=True).all()
    disponibles = []

    for h in habitaciones:
        ocupada = any(
            Reserva.query.filter_by(id=h.id, inicio=inicio + timedelta(days=i)).first()
            for i in range((fin - inicio).days + 1)
        )
        if not ocupada:
            disponibles.append(h)

    schema = HabitacionSchema(many=True)
    return jsonify(schema.dump(disponibles)), 200
