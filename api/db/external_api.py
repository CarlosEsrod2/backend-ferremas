import requests

class ExternalAPI:
    url = 'https://mindicador.cl/api/'
    @staticmethod
    def get_dollar_data():
        response = requests.get(ExternalAPI.url + 'dolar')
        if response.status_code == 200:
            data = response.json()
            #return data['serie'][0]['valor']
            return data
        else:
            raise Exception("Error al obtener el valor del dólar desde la API")