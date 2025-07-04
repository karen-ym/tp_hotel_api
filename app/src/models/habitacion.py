from dependencias import db

class Habitacion(db.Model):
    __tablename__ = "habitaciones"
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    estado = db.Column(db.Boolean, default=True)