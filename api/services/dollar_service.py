from api.models.dollar import Dollar
from api.db.external_api import ExternalAPI

class DollarService:
    def get_dollar_today(self):
        try:
            data = ExternalAPI.get_dollar_data()
            serie = data['serie'][0]
            return Dollar(fecha=serie['fecha'], valor=serie['valor']).to_dict()
        except Exception as e:
            #print(f"Error al obtener el valor del dólar: {e}")
            return {'error': 'API - mindicador.cl - no disponible'}