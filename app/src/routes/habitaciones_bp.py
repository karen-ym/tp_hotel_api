from flask import Blueprint, request, jsonify
from src.models.habitacion import Habitacion
from src.schemas.habitacion_schema import habitacion_schema, habitaciones_schema
from src.security.security import token_required
from marshmallow import ValidationError
from dependencias import db

habitaciones_bp = Blueprint("habitaciones_bp", __name__)


@habitaciones_bp.route("/habitaciones", methods=["GET"])
def listar():
    habitaciones = Habitacion.query.all()

    habitaciones_dump = habitaciones_schema.dump(habitaciones)
    return jsonify({"habitaciones": habitaciones_dump})

@habitaciones_bp.route("/habitaciones", methods=["POST"])
@token_required("Empleado")
def crear():
    data = request.get_json()
    try:
        nueva = habitacion_schema.load(data)
    except ValidationError as err:
        return jsonify({"errores": err.messages}), 400

    db.session.add(nueva)
    db.session.commit()
    return jsonify({"mensaje": "Se agrego correctamente"}), 201

@habitaciones_bp.route("/habitaciones/<int:id>/precio", methods=["PUT"])
@token_required("Empleado")
def editar(id):
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
@token_required("Empleado")
def desactivar(id):
    habitacion = Habitacion.query.get(id)
    if not habitacion:
        return jsonify({"mensaje": "No encontrada"}), 404
    habitacion.estado = False
    db.session.commit()
    return jsonify({"mensaje": "Desactivada"})

@habitaciones_bp.route("/habitaciones/<int:id>", methods=['POST'])
@token_required("Empleado")
def activar(id):
    habitacion = Habitacion.query.get(id)
    if not habitacion:
        return jsonify({"mensaje": "No encontrada"}), 404
    
    habitacion.estado = True
    db.session.commit()
    return jsonify({"mensaje": "Activada"})

@habitaciones_bp.route("/habitaciones/<int:id>", methods=['GET'])
@token_required("Empleado")
def info_habitacion(id):
    habitacion = Habitacion.query.get(id)
    if not habitacion:
        return jsonify({"mensaje": "No encontrada"}), 404
    #Falta agregar query de reservas
    return None