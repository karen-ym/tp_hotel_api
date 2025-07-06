from marshmallow import Schema, fields, validates, ValidationError
from dependencias import db, ma

class ReservaSchema(Schema):
    id = fields.Int(dump_only=True)
    habitacion_id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    inicio = fields.Date(required=True)
    fin = fields.Date(required=True)

    numero = fields.Int(attribute="habitacion.numero", dump_only=True)

    @validates("inicio")
    def validar_inicio(self, value):
        if not value:
            raise ValidationError("La fecha de inicio es requerida")

    @validates("fin")
    def validar_fin(self, value):
        if not value:
            raise ValidationError("La fecha de fin es requerida")
reservas_Schema = ReservaSchema(many=True)