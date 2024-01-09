from flask_restful import Resource, reqparse
from flask import g, request
from src import db, api
from src.models import Cart, CartItem, Order, Product
from src.jwt import token_required
from datetime import datetime

order_args = reqparse.RequestParser()
order_args.add_argument('cart_id', type=int, required=True)

class OrderResource(Resource):

    #-----------------------GET REQAUEST (ORDER HISTORY)-------------------------
    # @token_required('user')
    def get(self):
        try:
            user_id = request.args.get("user_id")
            order_history = Order.query.filter_by(user_id=user_id).all()

            result= []
            for order in order_history:
                product = Product.query.get(order.product_id)
                result.append({
                    "id":order.id,
                    "user_id":order.user_id,
                    "product_id":order.product_id,
                    "quantity":order.quantity,
                    "order_date":order.order_date.strftime("%Y-%m-%d %H:%M:%S") if order.order_date else None,
                    "product_name": product.product_name,
                })

            return result
                
        except Exception as e:
            print("Error:", str(e))
            return {"message": "Internal Server Error", "error": str(e)}, 500

    #------------------POST REQUEST (ORDERING ITEMS)------------------------------
    @token_required('user')
    def post(self):
        try:
            user_id = g.user.get('user_id')

            if user_id is None:
                return {"message": "User ID not found in token"}, 401

            args = order_args.parse_args()
            cart_id = args['cart_id']

            # Checking for items in cart
            cart_items = CartItem.query.filter_by(cart_id=cart_id, user_id=user_id).all()
            if not cart_items:
                return {'message': 'No items in the cart for the given user'}, 404

            # Populating Order table
            for cart_item in cart_items:
                product = Product.query.get(cart_item.product_id)
                quantity_left = product.quantity - cart_item.quantity
                if quantity_left >= 0:
                    order = Order(
                        user_id=user_id,
                        product_id=cart_item.product_id,
                        quantity=cart_item.quantity,
                        order_date=datetime.utcnow()
                    )
                    db.session.add(order)
                    product.quantity = quantity_left
                else:
                    cart_item.quantity = product.quantity
                    product.quantity = 0

            # Clearing cart after checkout is clicked and discarding cart
            CartItem.query.filter_by(cart_id=cart_id, user_id=user_id).delete()
            Cart.query.filter_by(user_id = user_id ).delete()
            db.session.commit()

            return {'message': 'Order placed successfully'}, 200

        except Exception as e:
            return {"message": "Internal Server Error", "error": str(e)}, 500

        
api.add_resource(OrderResource, '/orders')