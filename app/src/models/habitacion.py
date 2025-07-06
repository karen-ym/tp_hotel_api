from dependencias import db
from src.models.reserva import Reserva


class Habitacion(db.Model):
    __tablename__ = "habitaciones"
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    activa = db.Column(db.Boolean, default=True)

    
    reservas = db.relationship('Reserva', back_populates='habitacion')
