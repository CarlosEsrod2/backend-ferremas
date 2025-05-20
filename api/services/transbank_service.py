from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.integration_type import IntegrationType
import json

class TransbankService:
    def __init__(self):
        # Configuración para ambiente de prueba
        self.commerce_code = '597055555532'  # Código de comercio de prueba
        self.api_key = '579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C'  # API Key de prueba
        self.default_integration_type = IntegrationType.TEST  # Tipo de integración (TEST o LIVE)
        
        #Transaction.configure_for_integration(self.commerce_code, self.api_key, IntegrationType.TEST)
        #Transaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS, IntegrationApiKeys.WEBPAY, IntegrationType.TEST))
        #self.transbank.webpay.webpay_plus.default_integration_type = IntegrationType.TEST

    def create_transaction(self, buy_order, session_id, amount, return_url):
        """
        Crea una transacción en Webpay Plus
        
        Args:
            buy_order (str): Orden de compra. Debe ser único por transacción.
            session_id (str): Identificador de sesión. Opcional.
            amount (int): Monto de la transacción.
            return_url (str): URL a la que Webpay redirigirá post-transacción.
            
        Returns:
            dict: Respuesta de Webpay con URL de redirección y token
        """
        try:
            response = Transaction.create(buy_order, session_id, amount, return_url)
            return {
                'url': response.url,
                'token': response.token,
                'success': True
            }
        except Exception as e:
            return {
                'error': str(e),
                'success': False
            }

    def commit_transaction(self, token):
        """
        Confirma una transacción luego de que el usuario ha completado el flujo en Webpay
        
        Args:
            token (str): Token de la transacción
            
        Returns:
            dict: Resultado de la transacción
        """
        try:
            response = Transaction.commit(token)
            return {
                'response_code': response.response_code,
                'status': response.status,
                'amount': response.amount,
                'buy_order': response.buy_order,
                'session_id': response.session_id,
                'card_detail': response.card_detail,
                'accounting_date': response.accounting_date,
                'transaction_date': response.transaction_date,
                'authorization_code': response.authorization_code,
                'payment_type_code': response.payment_type_code,
                'installments_number': response.installments_number,
                'success': True
            }
        except Exception as e:
            print(f"Error al confirmar la transacción: {e}")
            return {
                'error': str(e),
                'success': False
            }