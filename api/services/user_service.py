from api.models.user import User

class UserService:
    def __init__(self, mysql):
        self.mysql = mysql
        
    def get_all_users(self):
        cursor = self.mysql.connection.cursor()
        cursor.execute("SELECT id, name, email, pass FROM users")
        results = cursor.fetchall()
        users = [User(id=row[0], name=row[1], email=row[2], pass_=row[3]).to_dict() for row in results]
        return users
    
    def register_user(self, name, email, password=None):
        cursor = self.mysql.connection.cursor()
        
        # Si no se proporciona contraseña, se usa 'pass' por defecto
        if password is None:
            password = 'pass'
        
        # Validar si ya existe el correo
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()
        if existing_user:
            return {"message": "El correo ya está registrado"}, 400

        # Insertar usuario si no existe
        cursor.execute("INSERT INTO users (name, email, pass) VALUES (%s, %s, %s)", 
                      (name, email, password))
        self.mysql.connection.commit()
        return {"message": f"Usuario {name} registrado y correo simulado enviado a {email}"}, 201

    def login_user(self, email, password=None):
        cursor = self.mysql.connection.cursor()
        
        if password:
            # Si se proporciona contraseña, se verifica junto con el correo
            cursor.execute("SELECT id, name, email FROM users WHERE email = %s AND pass = %s", 
                          (email, password))
        else:
            # Mantener compatibilidad con login solo por email (testeo, en caso de que no se pase la contraseña)
            cursor.execute("SELECT id, name, email FROM users WHERE email = %s", (email,))
            
        row = cursor.fetchone()
        if row:
            user = User(id=row[0], name=row[1], email=row[2])
            return user.to_dict(), 200
        else:
            return {"message": "Usuario no encontrado o contraseña incorrecta"}, 404