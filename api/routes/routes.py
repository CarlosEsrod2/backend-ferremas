from flask import Blueprint, request, jsonify
from api.services.user_service import UserService
from api.services.product_service import ProductService
from api.services.product_service_by_id import ProductServiceById
from api.services.email_service import enviar_correo_bienvenida

def register_routes(app, mysql):
    api_bp = Blueprint('api', __name__)

    user_service = UserService(mysql)
    product_service = ProductService(mysql)
    #product_service_by_id = ProductServiceById(mysql)

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
        if not name or not email:
            return jsonify({"message": "Faltan campos obligatorios"}), 400

        result, status_code = user_service.register_user(name, email)
        return jsonify(result), status_code

    @api_bp.route('/login', methods=['POST'])
    def login_user():
        data = request.get_json()
        email = data.get('email')
        if not email:
            return jsonify({"message": "Falta el email"}), 400

        result, status_code = user_service.login_user(email)
        return jsonify(result), status_code



    app.register_blueprint(api_bp)