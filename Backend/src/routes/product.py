from base64 import b64encode
from datetime import datetime
from sqlalchemy import and_
from src import api,db
from flask_restful import Resource, reqparse
from flask import request, send_file
from src.jwt import token_required
from src.models import Product
import os, werkzeug, io


# UPLOADING PRODUCT IMAGE
UPLOAD_FOLDER = "Product Images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


product_args = reqparse.RequestParser()
product_args.add_argument('product_image', type=werkzeug.datastructures.FileStorage, location="files", required=True, help="Please provide product image")
# product_args.add_argument('product_image', type=str, required=True, help="Please provide product image")
product_args.add_argument('product_name', type=str, location="form", required=True, help='Product name is required')
product_args.add_argument('quantity', type=int, location="form", required=True, help='Quantity is required')
product_args.add_argument('mfg_date', type=str, location="form", required=True, help='Manufacturing date is required')
product_args.add_argument('exp_date', type=str, location="form", required=True, help='Expiration date is required')
product_args.add_argument('rate_per_unit', type=float, location="form", required=True, help='Rate per unit is required')
product_args.add_argument('category_id', type=int, location="form", required=False, help='Category ID is required')

class ProductResource(Resource):

    #-------------------GET REQUEST-----------------------------------
    #Products should fall under a particular category. Each category should have their own kind of products.

    def get(self):
        query = request.args.get('query')
        category = request.args.get('category')
        min_price = request.args.get('min_price')
        max_price = request.args.get('max_price')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        if "product_id" in request.args:
            productId = request.args.get("product_id")
            
            if productId:
                product = Product.query.filter_by(id = productId).first()
                if product:
                    product_image_data = product.get_product_image_data()
                    result = {
                        "id": product.id,
                        "product_image": product_image_data,
                        "product_name": product.product_name,
                        "quantity": product.quantity,
                        "mfg_date": product.mfg_date.strftime("%d-%m-%Y") if product.mfg_date else None,
                        "exp_date": product.exp_date.strftime("%d-%m-%Y") if product.exp_date else None,
                        "rate_per_unit": product.rate_per_unit,
                        "category_id":product.category_id,
                    }
                    return result
                else:
                    return {"message": "Product not found."}, 404


        elif "category_id" in request.args:
            categoryId = request.args.get("category_id")
            result = []

            if categoryId:
                products = Product.query.filter_by(category_id=categoryId).all()
                if products:
                    for product in products:
                        product_image_data = product.get_product_image_data()
                        result.append({
                            "id": product.id,
                            "product_image": product_image_data,
                            "product_name": product.product_name,
                            "quantity": product.quantity,
                            "mfg_date": product.mfg_date.strftime("%d-%m-%Y") if product.mfg_date else None,
                            "exp_date": product.exp_date.strftime("%d-%m-%Y") if product.exp_date else None,
                            "rate_per_unit": product.rate_per_unit,
                            "category_id":product.category_id,
                        })
                    return result
                else:
                    return {"message": "No products found."}, 404
            else:
                return {"message": "Please select a category."}, 400
        else:
            products = Product.query.filter(
                and_(
                    (Product.product_name.ilike(f"%{query}%")) if query else True,
                    (Product.category_id == category) if category else True,
                    (Product.rate_per_unit >= min_price) if min_price else True,
                    (Product.rate_per_unit <= max_price) if max_price else True,
                    (Product.mfg_date >= start_date) if start_date else True,
                    (Product.mfg_date <= end_date) if end_date else True,
                )
            ).all()

            result = []
            for product in products:
                product_image_data = product.get_product_image_data()
                result.append({
                    "id": product.id,
                    "product_image": product_image_data,
                    "product_name": product.product_name,
                    "quantity": product.quantity,
                    "mfg_date": product.mfg_date.strftime("%d-%m-%Y") if product.mfg_date else None,
                    "exp_date": product.exp_date.strftime("%d-%m-%Y") if product.exp_date else None,
                    "rate_per_unit": product.rate_per_unit,
                    "category_id":product.category_id,
                })
            return result

    
    #----------------POST REQUEST--------------------------------------
    # @token_required('store_admin')
    def post(self):
        args = product_args.parse_args()

        mfg_date_str = args["mfg_date"]
        exp_date_str = args["exp_date"]

        try:
            args["mfg_date"] = datetime.strptime(mfg_date_str, "%Y-%m-%d")
            args["exp_date"] = datetime.strptime(exp_date_str, "%Y-%m-%d")
        except ValueError as e:
            return {"message": "Invalid date format. Use YYYY-MM-DD."}, 400

        #PRODUCT IMAGE
        product_image_file = args["product_image"]

        if not product_image_file or not product_image_file.filename:
            return {"message":"Please upload an image!"}, 400
        
        if not allowed_file(product_image_file.filename):
            return {"message":"Unsupported file format!"}
        
        #Converting product image in bytes
        prod_img_bytes = product_image_file.read()
        

        args["product_image"] = prod_img_bytes

        product = Product(**args)

        try:
            db.session.add(product)
            db.session.commit()
        except Exception as e:
            return {"message":"Something went wrong", "error": str(e)}, 500
        
        return {"message":"Product added successfully!"}

    #---------------PUT REQUEST----------------------------------------    
    # @token_required('store_admin')
    def put(self):

        args = product_args.parse_args()

        mfg_date_str = args["mfg_date"]
        exp_date_str = args["exp_date"]

        # try:
        #     args["mfg_date"] = datetime.strptime(mfg_date_str, "%Y-%m-%d")
        #     args["exp_date"] = datetime.strptime(exp_date_str, "%Y-%m-%d")
        # except ValueError as e:
        #     return {"message": "Invalid date format. Use YYYY-MM-DD."}, 400
        try:
            if "product_id" in request.args:
                productId = int(request.args["product_id"])
            else:
                return {"message": "Please provide product id"}, 404

        except ValueError:
            return {"message": "Product id should be integer"}, 400


        if productId:
            try:
                product = Product.query.filter_by(id=productId).first()

                if not product:
                    return {"message": "Product not found"}, 404

                # PRODUCT IMAGE
                product_image_file = args["product_image"]

                if product_image_file:
                    if not allowed_file(product_image_file.filename):
                        return {"message": "Unsupported file format!"}, 400

                    image_data = product_image_file.read()
                    args["product_image"] = image_data

                    # HANDLING DATES
                    args["mfg_date"] = datetime.strptime(args["mfg_date"], "%Y-%m-%d")
                    args["exp_date"] = datetime.strptime(args["exp_date"], "%Y-%m-%d")

                for key, value in args.items():
                    setattr(product, key, value)

                db.session.commit()
                return {"message": "Product details updated successfully"}

            except Exception as e:
                return {"message": "Something went wrong", "error": str(e)}, 500
            
    #-----------------DELETE REQUEST-----------------------------------

    # @token_required
    def delete(self):
        try:
            if "product_id" in request.args:
                productId = int(request.args["product_id"])
            else:
                return {"message":"Please provide product id"}, 404
            
        except ValueError:
            return {"message":"Product id should be integer"}, 400


        if productId:
            try:
                product = Product.query.filter_by(id = productId).first()

                if not product:
                    return {"message": "Product not found"}, 404
                
                db.session.delete(product)
                db.session.commit()
                return {"message":"Product deleted succesfully"}
            
            except Exception as e:
                return {"message":"Something went wrong", "error":str(e)}, 500
            

api.add_resource(ProductResource, '/products')
