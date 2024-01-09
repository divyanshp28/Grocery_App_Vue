from src import api,db
from flask_restful import Resource, reqparse
from flask import request, send_file
from src.jwt import token_required
from src.models import Category, User

category_args = reqparse.RequestParser()
category_args.add_argument('category_name', type=str, required=True, help='Category name is required')

class CategoryResource(Resource):

    #----------------------GET REQUEST--------------------
    # GET ALL CATEGORIES

    # @token_required
    def get(self):

        categoryId = request.args.get("category_id")

        if categoryId:
            category = Category.query.filter_by(id = categoryId).first()
            if category:
                return category.output
            return{"message":"Category not found!"}
        
        else:
            category = Category.query.all()
            result =  [i.output for i in category]
        return result
    
    #-----------POST REQUEST---------------------------
    @token_required('admin')
    def post(self):
        args = category_args.parse_args()

        category = Category(**args)

        try:
            db.session.add(category)
            db.session.commit()
        except Exception as e:
            return {"message":"Something went wrong", "error": str(e)}, 500
        
        return {"message":"Category added successfully!"}
    
    #----------PUT REQUEST----------------------------------------------

    @token_required('admin')
    def put(self):
        
        try:
            if "category_id" in request.args:
                categoryId = int(request.args["category_id"])
            else:
                return {"message":"Please provide category id"}, 404
            
        except ValueError:
            return {"message":"Category id should be integer"}, 400

        args = category_args.parse_args()

        if categoryId:
            try:
                category = Category.query.filter_by(id = categoryId).first()

                if not category:
                    return {"message": "Category not found"}, 404
                
                for key, value in args.items():
                    setattr(category, key, value)

                db.session.commit()
                return {"message":"Category details updated succesfully"}
            
            except Exception as e:
                return {"message":"Something went wrong", "error":str(e)}, 500
            
    #--------------DELETE REQUEST----------------------------------

    @token_required('admin')
    def delete(self):
        
        try:
            if "category_id" in request.args:
                categoryId = int(request.args["category_id"])
            else:
                return {"message":"Please provide category id"}, 404
            
        except ValueError:
            return {"message":"Category id should be integer"}, 400

        # args = category_args.parse_args()

        if categoryId:
            try:
                category = Category.query.filter_by(id = categoryId).first()

                if not category:
                    return {"message": "Category not found"}, 404
                
                db.session.delete(category)
                db.session.commit()
                return {"message":"Category deleted succesfully"}
            
            except Exception as e:
                return {"message":"Something went wrong", "error":str(e)}, 500


api.add_resource(CategoryResource, '/categories')
