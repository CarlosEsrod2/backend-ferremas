from flask import Blueprint, request, jsonify, url_for, redirect
from flask_cors import cross_origin
from api.services.user_service import UserService
from api.services.product_service import ProductService
from api.services.email_service import enviar_correo_bienvenida
from api.services.webpay_service import WebpayService 
import uuid
import datetime

def register_routes(app, mysql):
    api_bp = Blueprint('api', __name__)

    user_service = UserService(mysql)
    product_service = ProductService(mysql)
    webpay_service = WebpayService()

    @api_bp.route('/users', methods=['GET'])
    def get_users():
        users = user_service.get_all_users()
        return jsonify(users)

    @api_bp.route('/products', methods=['GET'])
    def get_products():
        products = product_service.get_all_products()
        return jsonify(products)
    
    @api_bp.route('/products/<int:product_id>', methods=['GET'])
    def get_product_by_id(product_id):
        product = product_service.get_product_by_id(product_id)
        if product:
            return jsonify(product)
        else:
            return jsonify({"message": "Product not found"}), 404
        
    @api_bp.route('/register', methods=['POST'])
    def register_user():
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password', 'pass')  # Contraseña opcional, por defecto 'pass'
        
        if not name or not email:
            return jsonify({"message": "Faltan campos obligatorios"}), 400

        result, status_code = user_service.register_user(name, email, password)
        # Intentar enviar correo de bienvenida (no bloquea el registro si falla)
        try:
            enviar_correo_bienvenida(email, name)
        except Exception as e:
            print(f"Error al enviar correo: {e}")
        
        return jsonify(result), status_code

    @api_bp.route('/login', methods=['POST'])
    def login_user():
        data = request.get_json()
        email = data.get('email')
        password = data.get('password') 
        
        if not email:
            return jsonify({"message": "Falta el email"}), 400

        # Si no hay contraseña, se usa el método anterior solo con email
        # Si hay contraseña, validamos ambos
        user, status_code = user_service.login_user(email, password)
        if status_code == 200:
            # Si el login es exitoso, añadimos información del descuento al usuario
            user['descuento'] = 10  # Descuento fijo del 10% MODIFICAR EN CASO DE SER NECESARIO
            
            return jsonify(user), status_code
        else:
            return jsonify({"success": False, "message": "Usuario no encontrado o contraseña incorrecta"}), status_code
    
    

    #######################################################
    ################# Transbank Routes ####################
    #######################################################
    @api_bp.route('/crear-transaccion', methods=['GET','POST'])
    def crear_transaccion():
        data = request.get_json()
        amount = data.get('amount', 0)
        try:
            # Iniciar transacción con WebPay
            response = webpay_service.iniciar_pago(amount)
            return jsonify(response)
        except Exception as e:
            app.logger.error(f"Error al crear transacción: {str(e)}")
            return jsonify({"success": False, "error": str(e)}), 500
        
        #url = webpay_service.iniciar_pago(data['amount'])
        #return redirect(url)

    @api_bp.route('/confirmar_pago', methods=['GET', 'POST'])
    def confirmar_pago():
        token = request.form.get("token_ws") or request.args.get("token_ws")
        
        if not token:
            return jsonify({"success": False, "message": "Token no proporcionado"}), 400
        
        try:
            response = webpay_service.confirmar_pago(token)
            # Procesar respuesta exitosa
            return redirect(f"{app.config['FRONTEND_URL']}/payment-result?status=success&order={response.get('buy_order', 'unknown')}")
        except Exception as e:
            app.logger.error(f"Error al confirmar pago: {str(e)}")
            # Redireccionar a página de error de pago
            return redirect(f"{app.config['FRONTEND_URL']}/payment-result?status=error&message={str(e)}")
        
    app.register_blueprint(api_bp)