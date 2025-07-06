from marshmallow import Schema, fields, validates, ValidationError
from dependencias import db, ma

class ReservaSchema(Schema):
    id = fields.Int(dump_only=True)
    habitacion_id = fields.Int(required=True)
    usuario_id = fields.Int(required=True)
    fecha = fields.Date(required=True)

    @validates("fecha")
    def validar_fecha(self, value):
        if not value:
            raise ValidationError("La fecha es requerida")

reservas_Schema = ReservaSchema(many=True)