from flask import Flask
from flask_cors import CORS
from api.routes.routes import register_routes
from api.db.database import init_db

app = Flask(__name__)

# Habilitar CORS (permite peticiones desde React)
CORS(app, origins=["http://localhost:3000"])

# Configuración MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '' 
app.config['MYSQL_DB'] = 'ferremas' # añadir el nombre de la base de datos

# URL del frontend para redirecciones
app.config['FRONTEND_URL'] = 'http://localhost:3000'

# Inicializar MySQL
mysql = init_db(app)

# Registrar las rutas y pasar mysql
register_routes(app, mysql)

if __name__ == '__main__':
    app.run(debug=True)
