# BLUEPRINT AUTH

from flask import Blueprint, request, jsonify, current_app
import jwt
from datetime import datetime, timedelta, timezone
from functools import wraps 
from src.security.security import token_required 

# Inicializamos el blue print
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