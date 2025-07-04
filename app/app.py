from flask import Flask
from src.routes.auth_bp import auth_bp 
from dependencias import db, ma
from src.routes.habitaciones_bp import habitaciones_bp

app = Flask(__name__)

db.init_app(app)
ma.init_app(app)

app.config["SECRET_KEY"] = "pass1234"  # Clave secreta para JWT (debería estar en una variable de entorno? chequear despues)

app.register_blueprint(auth_bp) # Registrar el blueprint
app.register_blueprint(habitaciones_bp)

@app.route("/")
def prueba():
  return "Hola!"

if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=5000) # En el .exe -> urlbase: http://localhost:5000