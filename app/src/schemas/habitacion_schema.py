from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow import fields, validate
from models.habitacion import Habitacion
from app import db

class HabitacionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Habitacion
        load_instance = True #activa la conversión dict → modelo. Devuelve un objeto Habitacion
        sqla_session = db.session  # Le damos la sesión de SQLAlchemy para poder construir el modelo

    id = auto_field(dump_only=True)

    numero = fields.Integer(
        required=True,
        validate=validate.Range(min=1),
    )

    precio = fields.Float(
        required=True,
        validate=validate.Range(min=0),
    )

    activa = fields.Boolean(load_default=True) 
habitacion_schema = HabitacionSchema()
habitaciones_schema = HabitacionSchema(many=True)