from flask_restful import Resource, reqparse
from flask import g, request
from src import db, api
from src.models import CartItem, Product
from src.jwt import token_required

cart_item_args = reqparse.RequestParser()
cart_item_args.add_argument('cart_id', type=int, required=True)
cart_item_args.add_argument('user_id', type=int, required=True)

class CartItemResource(Resource):
    #-------------------------------GET REQUEST--------------------------------
    @token_required('user')
    def get(self):
        try:
            user_id = g.user.get('user_id')
            cart_items = CartItem.query.filter_by(user_id=user_id).all()

            result = []
            for cart_item in cart_items:
                product = Product.query.get(cart_item.product_id)
                if product:
                    result.append({
                        "id": cart_item.id,
                        "cart_id": cart_item.cart_id,
                        "user_id": cart_item.user_id,
                        "product_id": cart_item.product_id,
                        "rate_per_unit": cart_item.rate_per_unit,
                        "quantity": cart_item.quantity,
                        "product_details": {
                            "product_image": product.get_product_image_data(),
                            "product_name": product.product_name,
                            "exp_date": product.exp_date.strftime("%d-%m-%Y") if product.exp_date else None,
                            "rate_per_unit": product.rate_per_unit,
                        }
                    })

            return result

        except Exception as e:
            return {"message": "Internal Server Error", "error": str(e)}, 500

    #-----------------------DELETE REQUEST-----------------------------------
    @token_required('user')
    def delete(self):
        try:
            if "item_id" in request.args:
                itemId = int(request.args["item_id"])
            else:
                return {"message":"Please provide cart item id"}, 404
        except ValueError:
            return {"message":"Cart item ID should be integer"}, 400
        
        if itemId:
            try:
                item = CartItem.query.filter_by(id=itemId).first()

                if not item:
                    return {"message":"Cart item not found"}, 404
                
                db.session.delete(item)
                db.session.commit()
                return {"message":"Cart item deleted successfully"}
            except Exception as e:
                return {"message":"Something went wrong", "error":str(e)}, 500
        

api.add_resource(CartItemResource, '/cart_items')
