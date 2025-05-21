from api.db.webpay_api import WebpayApi
from flask import jsonify

class WebpayService:
    def iniciar_pago(self, amount):
        buy_order = "12345678"
        return_url = "http://localhost:5000/confirmar_pago"
        session_id = "SessionId"
        transaction = WebpayApi.get_transaction()
        response = transaction.create(buy_order, session_id, amount, return_url)
        #return response['url'] + "?token_ws=" + response['token']
        return jsonify({
            "url": response['url'] + "?token_ws=" + response['token']
        })
    
    def confirmar_pago(self, token):
        transaction = WebpayApi.get_transaction()
        response = transaction.commit(token)
        return response