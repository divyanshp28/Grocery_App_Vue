# from src import api,db
# from flask_restful import Resource
# from flask import request
# from src.jwt import token_required
# from src.models import SuperAdmin
# import random

# class Super_Admin(Resource):
#     @token_required
#     def get(self):
#         if "id" in request.args:
#             admin = SuperAdmin.query.filter_by(id = request.args["id"]).first()
#             if not admin:
#                 return {"message":"User not found!"}, 404
#             return admin.output
#         super_admin = [i.output for i in SuperAdmin.query.all()]
#         return super_admin
    
# api.add_resource(Super_Admin, "/admin")
