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

### ES NECESARIO PRIMERO EJECUTARLO CON FLASK PARA CREAR LA DATABASE, LUEGO CON DOCKER PARA LA CORRER LA APP.

## Configuración de Entorno

Este proyecto utiliza variables de entorno para manejar claves secretas.

1.  Después de clonar el repositorio, crea una copia del archivo `.env.example` y renómbrala a `.env`.

2.  Abrí el nuevo archivo `.env`.

3.  Reemplazá el valor de `SECRET_KEY` por tu propia clave secreta.

4.  El archivo `.env` está ignorado por Git, por lo que las claves secretas nunca se suben.

## Ejecutar la Aplicación con Docker (Método para Entrega Final)

Este es el método recomendado y obligatorio. Utiliza Gunicorn dentro de un contenedor Docker.

**a. Descargar e iniciar Docker Desktop**

**b. Configurar la Conexión a la Base de Datos**

- Abre el archivo `app/app.py`.
- Busca la línea de `SQLALCHEMY_DATABASE_URI` (la que contiene host.docker.internal).
- Reemplaza con tus credenciales de PostgreSQL.

**c. Construir la Imagen Docker**
En la terminal, desde la carpeta raíz del proyecto, ejecuta:

```bash
docker build -t hotel-api .
```

**d. Ejecutar el Contenedor**
Una vez construida la imagen, inicia el contenedor:

```bash
docker run --name hotel-api-container -p 5000:5000 hotel-api
```
