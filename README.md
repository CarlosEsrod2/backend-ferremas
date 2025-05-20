# Ferremas API 🛠️ 

API REST para la gestión de productos e usuarios de Ferremas, con integración de pagos Transbank Webpay y conversión de precios a dólares.

## Características 📋 

- **Gestión de usuarios**: Registro, login y listado de usuarios
- **Gestión de productos**: Listado de productos con precios en CLP y USD
- **Integración con Transbank**: Pasarela de pagos para Chile
- **Conversión a dólares**: Integración con API mindicador.cl para obtener el valor actual del dólar

## Arquitectura Limpia 🏗️ 

El proyecto sigue los principios de Arquitectura Limpia con una clara separación de responsabilidades:

- **Capa de Presentación** (`routes`): Endpoints API y manejo de solicitudes HTTP
- **Capa de Aplicación** (`services`): Lógica de negocio y casos de uso
- **Capa de Dominio** (`models`): Entidades y reglas de negocio core
- **Capa de Infraestructura** (`db`): Acceso a bases de datos y servicios externos

## Estructura del Proyecto 🗂️ 

```
.
├── api/
│   ├── db/
│   │   ├── database.py         # Conexión a MySQL
│   │   └── external_api.py     # Cliente para API externa (mindicador.cl)
│   ├── models/
│   │   ├── dollar.py           # Entidad de conversión a dólar
│   │   ├── product.py          # Entidad de productos
│   │   └── user.py             # Entidad de usuarios
│   ├── routes/
│   │   └── routes.py           # Definición de endpoints HTTP
│   ├── services/
│   │   ├── dollar_service.py   # Servicio para obtener valor del dólar
│   │   ├── email_service.py    # Servicio para envío de emails
│   │   ├── product_service.py  # Lógica de productos
│   │   ├── transbank_service.py # Integración con Transbank
│   │   └── user_service.py     # Lógica de usuarios
│   └── utils/
│       └── helpers.py          # Funciones auxiliares
├── app.py                      # Punto de entrada de la aplicación
└── README.md                   # Este archivo
```

## Base de Datos 📊 

La aplicación utiliza MySQL con las siguientes tablas:

- **products**: Almacena información de productos (id, nombre, precio, tipo)
- **users**: Almacena información de usuarios (id, nombre, email, contraseña)

## Instalación y Configuración 🚀 

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/CarlosEsrod2/backend-ferremas.git
   cd backend-ferremas
   ```

2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Configurar base de datos MySQL:
   ```sql
   # Ejecutar el script SQL para crear la BD y tablas
   # Ver archivo: Creacion de tablas e insercion datos.sql
   ```

4. Configurar variables en `app.py`:
   ```python
   app.config['MYSQL_HOST'] = 'localhost'
   app.config['MYSQL_USER'] = 'root'
   app.config['MYSQL_PASSWORD'] = ''
   app.config['MYSQL_DB'] = 'ferremas'
   ```

5. Iniciar el servidor:
   ```bash
   py app.py
   ```

## Endpoints API 📡 

### Usuarios
- **GET /users**: Obtener todos los usuarios
- **POST /register**: Registrar nuevo usuario
- **POST /login**: Autenticar usuario

### Productos
- **GET /products**: Obtener todos los productos

### Transbank
- **POST /create-transaction**: Crear una transacción de pago
- **GET /transaction-commit**: Confirmar una transacción (usado por Transbank)

## Servicios Externos 🔄 

- **mindicador.cl**: API para obtener el valor actual del dólar
- **Transbank**: Pasarela de pagos para transacciones en Chile
- **SMTP**: Servicio para envío de correos electrónicos

## Lenguaje de Programación y Framework Utilizado 🧑‍💻

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)

Este proyecto fue desarrollado en **Python**, aprovechando su versatilidad y riqueza en librerías para el desarrollo backend con el framework **Flask**.


