from flask import Blueprint, request, jsonify
from src.models.habitacion import Habitacion
from src.schemas.habitacion_schema import habitacion_schema, habitaciones_schema
from src.security.security import token_required
from marshmallow import ValidationError
from dependencias import db
from src.models.reserva import Reserva
from src.schemas.reserva_schema import reservas_Schema


habitaciones_bp = Blueprint("habitaciones_bp", __name__)


@habitaciones_bp.route("/habitaciones", methods=["GET"])
def listar():
    habitaciones = Habitacion.query.all()

    habitaciones_dump = habitaciones_schema.dump(habitaciones)
    return jsonify({"habitaciones": habitaciones_dump})

@habitaciones_bp.route("/habitaciones", methods=["POST"])
@token_required("empleado")
def crear(current_user):
    data = request.get_json()
    try:
        nueva = habitacion_schema.load(data)
    except ValidationError as err:
        return jsonify({"errores": err.messages}), 400

    db.session.add(nueva)
    db.session.commit()
    return jsonify({"mensaje": "Se agrego correctamente"}), 201

@habitaciones_bp.route("/habitaciones/<int:id>/precio", methods=["PUT"])
@token_required("empleado")
def editar(current_user,id):
    habitacion = Habitacion.query.get(id)
    if not habitacion:
        return jsonify({"mensaje": "No encontrada"}), 404
    data = request.get_json()
    for key in ["numero", "precio", "estado"]:
        if key in data:
            setattr(habitacion, key, data[key])
    db.session.commit()
    return jsonify({"mensaje": "Se actualizo correctamente"})

@habitaciones_bp.route("/habitaciones/<int:id>", methods=["DELETE"])
@token_required("empleado")
def desactivar(current_user,id):
    habitacion = Habitacion.query.get(id)
    if not habitacion:
        return jsonify({"mensaje": "No encontrada"}), 404
    habitacion.activa = False
    db.session.commit()
    return jsonify({"mensaje": "Desactivada"})

@habitaciones_bp.route("/habitaciones/<int:id>", methods=['POST'])
@token_required("empleado")
def activar(current_user,id):
    habitacion = Habitacion.query.get(id)
    if not habitacion:
        return jsonify({"mensaje": "No encontrada"}), 404
    
    habitacion.activa = True
    db.session.commit()
    return jsonify({"mensaje": "Activada"})

@habitaciones_bp.route("/habitaciones/<int:id>", methods=['GET'])
@token_required("empleado")
def info_habitacion(current_user,id):
    habitacion = Habitacion.query.get(id)
    if not habitacion:
        return jsonify({"mensaje": "No encontrada"}), 404
    reservas = Reserva.query.filter(habitacion.id==id).all()

    habitacion_json = habitacion_schema.dump(habitacion)
    reservas_json = reservas_Schema.dump(reservas)

    habitacion_json["reservas"] = reservas_json
    
    return jsonify(habitacion_json)