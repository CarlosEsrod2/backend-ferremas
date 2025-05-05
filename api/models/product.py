class Product:
    def __init__(self, id, name, price, type):
        self.id = id
        self.name = name
        self.price = price
        self.type = type

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'type': self.type
        }
