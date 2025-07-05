from dependencias import db

class User(db.Model):
  __tablename__ = 'users'
  
  # Le pongo los nombres en inglés porque la consigna pide que sean =! a los que se esperan en los endpoints (usuario, clave, categoria)
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  password = db.Column(db.String(255), nullable=False) # chequear si entra el hash aca
  role = db.Column(db.String(50), nullable=False)