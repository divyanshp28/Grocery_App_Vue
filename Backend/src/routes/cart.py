from flask_restful import Resource, reqparse
from flask import g
from src import db, api
from src.models import Cart, CartItem, Product
from src.jwt import token_required

cart_args = reqparse.RequestParser()
cart_args.add_argument('user_id', type=int, required=True, help='User id is required')  
cart_args.add_argument('product_id', type=int, required=True, help='Product id is required')
cart_args.add_argument('quantity', type=int, required=True, help='Quantity is required')

class CartResource(Resource):
    #----------------------GET REQUEST----------------------------------------
    @token_required('user')
    def get(self):
        try:
            user_id = g.user.get('user_id')
            if user_id is None:
                return {"message": "User ID not found in token"}, 401

            cart = Cart.query.filter_by(user_id=user_id).first()

            if cart is None:
                return {'cart_items': [], 'cart_items_count': 0, 'total_cost': 0}

            cart_items = CartItem.query.filter_by(cart_id=cart.id).all()
            cart_items_count = len(cart_items)
            total_cost = sum(item.quantity * item.rate_per_unit for item in cart_items)

            for cart_item in cart_items:
                product = Product.query.get(cart_item.product_id)
                cart_item.product_name = product.product_name

            return {'user_id': user_id, 'cart_items': cart_items, 'cart_items_count': cart_items_count, 'total_cost': total_cost}

        except Exception as e:
            return {"message": "Internal Server Error", "error": str(e)}, 500
    

    #-------------------POST REQUEST-------------------------------------------------
    @token_required('user')
    def post(self):
        try:
            user_id = g.user.get('user_id')
            if user_id is None:
                return {"message": "User ID not found in token"}, 401

            args = cart_args.parse_args()
            product_id = args['product_id']
            quantity = args['quantity']

            # Checking if product exists
            product = Product.query.get(product_id)
            if product is None:
                return {'message': 'Product not found'}, 404

            # Checking if user has a cart else creating a cart
            cart = Cart.query.filter_by(user_id=user_id).first()
            if cart is None:
                cart = Cart(user_id=user_id, product_id=product_id, quantity=quantity)
                db.session.add(cart)
                db.session.commit()

            # Checking if the product is already in the cart if yes, then increasing it's quantity else adding it
            cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()

            if cart_item:
                cart_item.quantity += quantity
            else:
                cart_item = CartItem(
                    product_id=product_id,
                    quantity=quantity,
                    rate_per_unit=product.rate_per_unit,  
                    user_id=user_id,
                    cart_id=cart.id
                )
                db.session.add(cart_item)

            db.session.commit()
            return {'message': 'Product added to cart successfully'}, 200

        except Exception as e:
            return {"message": "Internal Server Error", "error": str(e)}, 500



api.add_resource(CartResource, '/cart')