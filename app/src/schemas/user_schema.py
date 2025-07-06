from dependencias import ma
from marshmallow import fields, validate

class UserSchema(ma.Schema):
  # Los nombres coinciden con lo que espera el endpoint del .exe (endpoint != atributo en db)

  usuario = fields.Str(
    required=True,
    error_messages={"required": "El nombre de usuario es obligatorio."}
  )
  categoria = fields.Str(
    required=True,
    validate=validate.OneOf(["cliente", "empleado"], error="La categoría debe ser 'Cliente' o 'Empleado'."),
    error_messages={"required": "La categoria es obligatoria."}
  )
  clave1 = fields.Str(
    required=True,
    error_messages={"required": "La clave es obligatoria."}
  )
  clave2 = fields.Str(
    required=True,
    error_messages={"required": "La confirmacion de la clave es obligatoria."}
  )

  class Meta:
    fields = ("usuario", "categoria", "clave1", "clave2")

# Instancia del schema 
user_schema = UserSchema()