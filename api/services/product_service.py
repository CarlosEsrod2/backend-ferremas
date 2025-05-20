import datetime
import json
import requests 
from api.models.product import Product
from api.services.dollar_service import DollarService

class ProductService:
    def __init__(self, mysql):
        self.mysql = mysql

    def get_all_products(self):
        cursor = self.mysql.connection.cursor()
        cursor.execute("SELECT id, name, price, type FROM product")
        results = cursor.fetchall()
        flag = False
        allproducts = []
        dollar_service = DollarService()

        try:
            # Obtener el valor del dólar desde la API
            valor_dolar = dollar_service.get_dollar_today()
            valor_dolar = valor_dolar['valor']
            flag = True
        except Exception as e:
            print(f"Error al obtener el valor del dólar: {e}")
            valor_dolar = 'API - mindicador.cl - no disponible'

        
        for row in results:
            products = Product(id=row[0], name=row[1], price=row[2], type=row[3]).to_dict()
            if flag:
                products['valor_dolar'] = round(row[2]/valor_dolar,2)
            else:
                products['valor_dolar'] = valor_dolar
            allproducts.append(products)
        
        #print(allproducts)
        return allproducts
    
    
    """
    def get_all_products(self):
        cursor = self.mysql.connection.cursor()
        cursor.execute("SELECT id, name, price, type FROM product")
        results = cursor.fetchall()
        flag = False
        allproducts = []
        try:
            # Obtener el valor del dólar desde la API
            date = datetime.date.today()
            dmy = date.strftime("%d-%m-%Y")
            url = f'https://mindicador.cl/api/dolar/{dmy}'
            response = requests.get(url)
            data = json.loads(response.text.encode("utf-8"))
            valor_dolar = data['serie'][0]['valor']
            flag = True
        except Exception as e:
            #print(f"Error al obtener el valor del dólar: {e}")
            valor_dolar = 'API - mindicador.cl - no disponible'

        for row in results:
            products = Product(id=row[0], name=row[1], price=row[2], type=row[3]).to_dict()
            if flag:
                products['valor_dolar'] = round(row[2]/valor_dolar,2)
            else:
                products['valor_dolar'] = valor_dolar
            allproducts.append(products)
        
        #print(allproducts)
        return allproducts
    """