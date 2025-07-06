# API de Gestión Hotelera

API realizada con Python y Flask (framework) para gestionar las habitaciones y reservas de un hotel, como parte de un trabajo práctico.

## Integrantes

- _Jorge Poma_
- _David Vasquez_
- _Karen Morel_

## Tecnologías Utilizadas

- Python 3.12.4
- PyJWT (JSON Web Tokens)
- PostgreSql
- Docker
- Flask
- Sql Alchemy
- Blueprint
- Marshmallow

---

## Instrucciones de Instalación y Montaje

Seguí estos pasos para montar la aplicación:

**1. Clonar el Repositorio**

```bash
git clone https://github.com/tu-usuario/tu-repositorio.git
cd tu-repositorio
```

**2. Crear el entorno (solo una vez)**

```bash
python -m venv venv
```

**3. Activar el entorno (se debe hacer cada vez que se empieza a trabajar)**

```bash
.\venv\Scripts\activate
```

**4. Instalar las Dependencias**
(Asegurate de que tu entorno virtual esté activado)

```bash
pip install -r requirements.txt
```

**5. Cambiar connection string:**

Buscar en app.py esta línea de código y completar con los valores de su db pgadmin:

```bash
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://nombreUsuario:clave@localhost:5432/hotel_api_db'
```

## Configuración de Entorno

Este proyecto utiliza variables de entorno para manejar claves secretas.

1.  Después de clonar el repositorio, crea una copia del archivo `.env.example` y renómbrala a `.env`.

2.  Abrí el nuevo archivo `.env`.

3.  Reemplazá el valor de `SECRET_KEY` por tu propia clave secreta.

4.  El archivo `.env` está ignorado por Git, por lo que las claves secretas nunca se suben.
