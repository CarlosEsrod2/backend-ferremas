from api.models.product import Product

class ProductService:
    def __init__(self, mysql):
        self.mysql = mysql

    def get_all_products(self):
        cursor = self.mysql.connection.cursor()
        cursor.execute("SELECT id, name, price, type FROM product")
        results = cursor.fetchall()
        products = [Product(id=row[0], name=row[1], price=row[2], type=row[3]).to_dict() for row in results]
        return products
    
    def get_product_by_id(self, product_id):
        cursor = self.mysql.connection.cursor()
        cursor.execute("SELECT id, name, price, type FROM product WHERE id = %s", (product_id,))
        row = cursor.fetchone()
        if row:
            product = Product(id=row[0], name=row[1], price=row[2], type=row[3])
            return product.to_dict()
        return None