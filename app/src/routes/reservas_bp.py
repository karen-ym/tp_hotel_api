from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from src.models.reserva import Reserva
from src.schemas.reserva_schema import ReservaSchema
from dependencias import db
from src.security.security import token_required
from src.models.habitacion import Habitacion
from src.models.user import User

reservas_bp = Blueprint("reservas_bp", __name__)

#Endpoint1: alta de reserva por rango de fechas (Cliente)
@reservas_bp.route("/reservas", methods=["POST"])
@token_required("cliente")
def crear_reserva(current_user):

    usuario = current_user["sub"]

    user_obj = User.query.filter_by(username=usuario).first()

    id_usuario = user_obj.id

    data = request.get_json()


    habitacion_id = data["habitacion"]
    inicio = datetime.strptime(data["inicio"], "%d/%m/%Y").date()
    fin = datetime.strptime(data["fin"], "%d/%m/%Y").date()
   

    if fin < inicio:
        return jsonify({"mensaje": "La fecha de fin no puede ser anterior a la de inicio"}), 400

    habitacion = Habitacion.query.get(habitacion_id)
    if not habitacion or not habitacion.activa:
        return jsonify({"mensaje": "Habitación no válida o no disponible"}), 400

    # Obtener lista de fechas
    fechas_reserva = [inicio + timedelta(days=i) for i in range((fin - inicio).days + 1)]

    # Verificar disponibilidad en todas las fechas
    fechas_ocupadas = [
        fecha for fecha in fechas_reserva
        if Reserva.query.filter_by(habitacion_id=habitacion_id, fecha=fecha).first()
    ]
    if fechas_ocupadas:
        fechas_str = ', '.join([f.strftime("%d/m/%Y") for f in fechas_ocupadas])
        return jsonify({"mensaje": f"La habitación ya está reservada en: {fechas_str}"}), 400

    # Crear reservas
    reservas = [
        Reserva(habitacion_id=habitacion_id, user_id=id_usuario, fecha=fecha)
        for fecha in fechas_reserva
    ]
    db.session.add_all(reservas)
    db.session.commit()

    return jsonify({"mensaje": "Reserva realizada con éxito"}), 201



#Endpoint 2: listado de todas las reservas (Empleado)
@reservas_bp.route("/reservas", methods=["GET"])
@token_required("empleado")
def listar_reservas(current_user):
    reservas = Reserva.query.all()
    schema = ReservaSchema(many=True)
    return jsonify(schema.dump(reservas)), 200