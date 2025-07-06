from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow import fields, validate
from src.models.habitacion import Habitacion
from dependencias import db

class HabitacionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Habitacion
        load_instance = True #activa la conversión dict → modelo. Devuelve un objeto Habitacion
        sqla_session = db.session  # Le damos la sesión de SQLAlchemy para poder construir el modelo

    #mapeo de los campos del modelo Habitacion y validaciones para serializar y deserializar
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

#Serializar y deserializar una sola habitación
habitacion_schema = HabitacionSchema()
#Serializar y deserializa una lista
habitaciones_schema = HabitacionSchema(many=True)