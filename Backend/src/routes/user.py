from src import api,db
from flask_restful import Resource
from flask import request
from src.jwt import token_required
from src.models import User
import random

class UserResource(Resource):
    # # @token_required
    # def get(self):

    #     userId = request.args.get("user_id")

    #     if userId:
    #         user = User.query.filter_by(id = request.args["user_id"]).first()

    #         if not user:
    #             return {"message":"User not found!"}, 404
    #         return user.output
    #     else:
    #         user = User.query.all()
    #         result = [i.output for i in user]
    #         return result
    
    # @token_required
    def get(self):
        username = request.args.get("username")

        if username:
            user = User.query.filter_by(username=username).first()

            if not user:
                return {"message": "User not found!"}, 404
            return user.output
        else:
            users = User.query.all()
            result = [i.output for i in users]
            return result

api.add_resource(UserResource, "/users")