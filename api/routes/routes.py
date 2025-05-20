from flask import Blueprint, request, jsonify, url_for, redirect
from api.services.user_service import UserService
from api.services.product_service import ProductService
from api.services.email_service import enviar_correo_bienvenida
from api.services.transbank_service import TransbankService
import uuid
import datetime

def register_routes(app, mysql):
    api_bp = Blueprint('api', __name__)

    user_service = UserService(mysql)
    product_service = ProductService(mysql)
    transbank_service = TransbankService()

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
    @api_bp.route('/create-transaction', methods=['POST']) #ERROR POST http://localhost:5000/create-transaction 500 (INTERNAL SERVER ERROR)
    def create_transaction():
        data = request.get_json()
        
        if not data or 'amount' not in data:
            return jsonify({"message": "Falta el monto de la transacción"}), 400
        
        amount = int(data['amount'])
        buy_order = f"BO-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:8]}"
        session_id = data.get('sessionId', str(uuid.uuid4()))
        
        # URL a la que Webpay redirigirá después de la transacción
        return_url = request.url_root.rstrip('/') + url_for('api.transaction_commit')
        
        response = transbank_service.create_transaction(buy_order, session_id, amount, return_url)
        
        if response['success']:
            return jsonify(response), 200
        else:
            return jsonify(response), 500
    
    @api_bp.route('/transaction-commit', methods=['GET'])
    def transaction_commit():
        token_ws = request.args.get('token_ws')
        
        if not token_ws:
            return jsonify({"message": "Token no recibido"}), 400
        
        response = transbank_service.commit_transaction(token_ws)
        
        # Crear una URL para redireccionar al frontend con los resultados
        if response['success']:
            redirect_url = f"{app.config.get('FRONTEND_URL', 'http://localhost:3000')}/payment-result?status=success&order={response['buy_order']}"
        else:
            redirect_url = f"{app.config.get('FRONTEND_URL', 'http://localhost:3000')}/payment-result?status=error"
        
        # Redirección al frontend con los resultados
        return redirect(redirect_url)
        
    app.register_blueprint(api_bp)