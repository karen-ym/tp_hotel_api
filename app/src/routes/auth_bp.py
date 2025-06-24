# BLUEPRINT AUTH

from flask import Blueprint, request, jsonify

# Inicializamos el blue print
auth_bp = Blueprint('auth', __name__)  # (nombreDelBlueprint, nombreParaFlask)

@auth_bp.route("/login", methods=["POST"])
def login():
  # Acá va la lógica JWT y tema tokens

  respuesta = {
    "token": "placeholder",
    "categoria": "cliente_empleado"
  }

  return jsonify(respuesta), 200

