from flask import Blueprint, request, jsonify, current_app
import jwt
from datetime import datetime, timedelta, timezone
from dependencias import db
from marshmallow import ValidationError 
from src.models.user import User
from src.schemas.user_schema import user_schema
from src.security.security import hash_password, check_password, token_required

# Iniciar el blue print
auth_bp = Blueprint('auth', __name__)  # (nombreDelBlueprint, nombreParaFlask)

@auth_bp.route("/login", methods=["POST"])
def login():
  # Acá va la lógica JWT y tema tokens
  data = request.get_json()
  if not data or not data.get('usuario') or not data.get('clave'):
    return jsonify({"message": "Faltan credenciales"}), 400
  
  username = data.get('usuario')
  password = data.get('clave')

  # -Simulación de base de datos-
  users = {
        "empleado1": {"password": "123", "role": "Empleado"},
        "cliente1": {"password": "456", "role": "Cliente"}
    }
  
  user_info = users.get(username)

  # Usuario ? ∃ // contraseña ? ∃
  if user_info and user_info["password"] == password:
    token = jwt.encode({
        'sub': username, # Identificador del usuario (subject)
        'role': user_info['role'], 
        'exp': datetime.now(timezone.utc) + timedelta(minutes=30)
    }, current_app.config['SECRET_KEY'], algorithm="HS256")

    return jsonify({
        "token": token,
        "categoria": user_info['role']
    }), 200
  else:
    return jsonify({"message": "Credenciales invalidas"}), 401



@auth_bp.route("/registro", methods=["POST"])
def registro():
  data = request.get_json()
  
  # Validar los datos de entrada con el schema Marshmallow
  try:
    datos_validos = user_schema.load(data)
  except ValidationError as err:
    return jsonify(err.messages), 400

  if datos_validos['clave1'] != datos_validos['clave2']:
    return jsonify({"message": "Las claves no coinciden"}), 400

  user_existente = User.query.filter_by(username=datos_validos['usuario']).first()
  if user_existente:
    return jsonify({"message": "El nombre de usuario ya está en uso"}), 400
  
  hashed_password = hash_password(datos_validos['clave1']) # Esta definido en security.py

  new_user = User(
      username=datos_validos['usuario'],
      password=hashed_password,
      role=datos_validos['categoria']
  )

  db.session.add(new_user)
  db.session.commit()

  return jsonify({"message": "Usuario registrado con éxito"}), 201 # 201 = "Created"