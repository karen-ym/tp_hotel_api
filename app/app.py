from flask import Flask
from dependencias import db, ma

def create_app():

  app = Flask(__name__)
  app.config["SECRET_KEY"] = "pass1234"  # Clave secreta para JWT (debería estar en una variable de entorno? chequear despues)

  app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://nombreUsuario:clave@localhost:5432/hotel_api_db' # -> COMPLETAR CON LOS DATOS DE LA DB DE USTDS (hotel_api_db es el nombre de la db, llamenla así.)
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

  from src.models.user import User

  db.init_app(app)
  ma.init_app(app)

  from src.routes.auth_bp import auth_bp
  from src.routes.habitaciones_bp import habitaciones_bp
  from src.routes.reservas_bp import reservas_bp 

  app.register_blueprint(auth_bp) # Registrar el blueprint
  app.register_blueprint(habitaciones_bp)
  app.register_blueprint(reservas_bp) 
  
  return app

if __name__ == "__main__":
  app = create_app()

  with app.app_context():
    db.create_all()  # Crea las tablas en la base de datos (SI no existen)

  app.run(debug=True, host="0.0.0.0", port=5000) # En el .exe -> urlbase: http://localhost:5000