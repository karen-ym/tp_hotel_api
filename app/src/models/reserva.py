from dependencias import db

class Reserva(db.Model):
    __tablename__ = "reservas"

    id = db.Column(db.Integer, primary_key=True)
    habitacion_id = db.Column(db.Integer, db.ForeignKey("habitaciones.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    fecha = db.Column(db.Date, nullable=False)

    habitacion = db.relationship('Habitacion', back_populates='reservas')
    user = db.relationship('User', back_populates='reservas')

