from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from src.models.reserva import Reserva
from src.schemas.reserva_schema import ReservaSchema
from src.models.habitacion import Habitacion
from src.schemas.habitacion_schema import HabitacionSchema
from src.security.security import token_required
from dependencias import db

reservas_bp = Blueprint("reservas_bp", __name__)

# Endpoints Clientes: Reserva un rango de fechas, ve habitaciones disponibles, ve estado de habitaciones en un día, y busca por precio 
# Endpoint 1:
@reservas_bp.route("/reservar", methods=["POST"])
@token_required("Cliente")
def reservar(current_user):
    data = request.get_json()
    habitacion_id = data["habitacion_id"]
    inicio = datetime.strptime(data["inicio"], "%Y-%m-%d")
    fin = datetime.strptime(data["fin"], "%Y-%m-%d")

    if fin < inicio:
        return jsonify({"error": "La fecha de fin no puede ser anterior a la de inicio"}), 400

    for i in range((fin - inicio).days + 1):
        fecha = inicio + timedelta(days=i)
        if Reserva.query.filter_by(habitacion_id=habitacion_id, fecha=fecha).first():
            return jsonify({"error": f"Ya reservada el {fecha.date()}"}), 400

    for i in range((fin - inicio).days + 1):
        fecha = inicio + timedelta(days=i)
        reserva = Reserva(habitacion_id=habitacion_id, usuario_id=current_user["id"], fecha=fecha)
        db.session.add(reserva)

    db.session.commit()
    return jsonify({"mensaje": "Reserva realizada con éxito"}), 201

# Endpoint 2:
@reservas_bp.route("/disponibles", methods=["GET"])
@token_required("Cliente")
def disponibles_rango(current_user):
    inicio = datetime.strptime(request.args.get("inicio"), "%Y-%m-%d")
    fin = datetime.strptime(request.args.get("fin"), "%Y-%m-%d")

    if fin < inicio:
        return jsonify({"error": "La fecha de fin no puede ser anterior a la de inicio"}), 400

    habitaciones = Habitacion.query.filter_by(estado=True).all()
    disponibles = []

    for h in habitaciones:
        ocupada = any(
            Reserva.query.filter_by(habitacion_id=h.id, fecha=inicio + timedelta(days=i)).first()
            for i in range((fin - inicio).days + 1)
        )
        if not ocupada:
            disponibles.append(h)

    schema = HabitacionSchema(many=True)
    return jsonify(schema.dump(disponibles)), 200

# Endpoint 3:
@reservas_bp.route("/estado-dia", methods=["GET"])
@token_required("Cliente")
def estado_dia(current_user):
    fecha = datetime.strptime(request.args.get("fecha"), "%Y-%m-%d").date()
    habitaciones = Habitacion.query.all()
    resultados = []

    for h in habitaciones:
        reservada = Reserva.query.filter_by(habitacion_id=h.id, fecha=fecha).first() is not None
        resultados.append({
            "numero": h.numero,
            "precio": h.precio,
            "estado": "ocupada" if reservada else "disponible"
        })

    return jsonify(resultados), 200

# Endpoint 4:
@reservas_bp.route("/precio-menor", methods=["GET"])
@token_required("Cliente")
def buscar_por_precio(current_user):
    limite = float(request.args.get("limite"))
    habitaciones = Habitacion.query.filter(Habitacion.precio <= limite, Habitacion.estado == True).all()
    schema = HabitacionSchema(many=True)
    return jsonify(schema.dump(habitaciones)), 200

# Endpoints Empleados: Crea reserva para un día específico y ve habitacion por número con reservas 
#Endpoint 1:
@reservas_bp.route("/reservar-dia", methods=["POST"])
@token_required("Empleado")
def reservar_dia(current_user):
    data = request.get_json()
    fecha = datetime.strptime(data["fecha"], "%Y-%m-%d").date()
    habitacion_id = data["habitacion_id"]
    usuario_id = data["usuario_id"]

    if Reserva.query.filter_by(habitacion_id=habitacion_id, fecha=fecha).first():
        return jsonify({"error": f"La habitación ya está reservada el {fecha}"}), 400

    reserva = Reserva(habitacion_id=habitacion_id, usuario_id=usuario_id, fecha=fecha)
    db.session.add(reserva)
    db.session.commit()
    return jsonify({"mensaje": "Reserva cargada con éxito"}), 201

# Endpoint 2:
@reservas_bp.route("/habitacion/<int:numero>", methods=["GET"])
@token_required("Empleado")
def ver_habitacion(current_user, numero):
    habitacion = Habitacion.query.filter_by(numero=numero).first()
    if not habitacion:
        return jsonify({"error": "Habitación no encontrada"}), 404

    reservas = Reserva.query.filter_by(habitacion_id=habitacion.id).all()
    schema = ReservaSchema(many=True)
    return jsonify({
        "numero": habitacion.numero,
        "precio": habitacion.precio,
        "reservas": schema.dump(reservas)
    }), 200