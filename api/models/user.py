class User:
    def __init__(self, id, name, email, pass_=None):
        self.id = id
        self.name = name
        self.email = email
        self.pass_ = pass_

    def to_dict(self):
        user_dict = {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }
        # Se incluye la contraseña en el diccionario si existe
        if self.pass_:
            user_dict['pass'] = self.pass_
        return user_dict