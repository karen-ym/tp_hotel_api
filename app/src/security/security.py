from functools import wraps
from flask import request, jsonify, current_app
import jwt
import hashlib
import os
import hmac

# Constructor de decoradores (pedido por el profesor)
def token_required(role_required):
    def decorator(f): # f = función a 'decorar'
        @wraps(f)

        def wrapper(*args, **kwargs):
            token = None
            # 1. Extraer el token del encabezado 'n-auth'
            if 'n-auth' in request.headers:
                
                # Quitar el bearer:
                try:
                    token = request.headers['n-auth'].split(" ")[1]
                except IndexError:
                    return jsonify({"message": "Formato de token inválido. Debe ser 'bearer <token>'."}), 401

            if not token:
                return jsonify({"message": "Token no encontrado."}), 401

            try:
                # 2. Decodificar el token usando la clave secreta de la app
                data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
                
                # 3. Verificar que el rol del token coincide con el rol requerido por la ruta
                if data['role'] != role_required:
                    return jsonify({"message": f"Acceso denegado. Se requiere ser '{role_required}'."}), 403 # 403 Forbidden

                # Si todo está bien, guardamos los datos del usuario
                current_user = data

            except jwt.ExpiredSignatureError:
                return jsonify({"message": "El token ha expirado."}), 401
            except jwt.InvalidTokenError:
                return jsonify({"message": "Token inválido."}), 401
            
            # 4. Ejecutar la función original de la ruta
            return f(current_user, *args, **kwargs)
        return wrapper
    return decorator

# ——— hashing de contraseñas ———

def hash_password(password):
  salt = os.urandom(16)  # Genera un salt aleatorio de 16 bytes
  pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000) # 'sha256' = algoritmo de hash
  storage = salt.hex() + ':' + pwd_hash.hex()
  return storage

def check_password(stored_password, provided_password):
  try:
    salt_hex, hash_hex = stored_password.split(':')
    salt = bytes.fromhex(salt_hex)
  except ValueError:
    return False
  
  pwd_hash = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt, 100000) # se hashea de igual manera (idem salt)
  return hmac.compare_digest(pwd_hash, bytes.fromhex(hash_hex)) #compara los dos hashes 