from api.models.user import User

class UserService:
    def __init__(self, mysql):
        self.mysql = mysql

    def get_all_users(self):
        cursor = self.mysql.connection.cursor()
        cursor.execute("SELECT id, name, email FROM users")
        results = cursor.fetchall()
        users = [User(id=row[0], name=row[1], email=row[2]).to_dict() for row in results]
        return users
    
    def register_user(self, name, email):
        cursor = self.mysql.connection.cursor()
        
        # Validar si ya existe el correo
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()
        if existing_user:
            return {"message": "El correo ya está registrado"}, 400

        # Insertar usuario si no existe
        cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
        self.mysql.connection.commit()
        return {"message": f"Usuario {name} registrado y correo simulado enviado a {email}"}, 201

    def login_user(self, email):
        cursor = self.mysql.connection.cursor()
        cursor.execute("SELECT id, name, email FROM users WHERE email = %s", (email,))
        row = cursor.fetchone()
        if row:
            user = User(id=row[0], name=row[1], email=row[2])
            return user.to_dict(), 200
        else:
            return {"message": "Usuario no encontrado"}, 404
