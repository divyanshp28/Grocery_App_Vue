# from src import api, db
# from flask_restful import Resource, reqparse
# from src.jwt import token_required, create_token, secret_token_key
# from src.models import StoreAdmin
# import jwt

# #---------------------STORE ADMIN SIGNUP---------------
# register_fields = ["username", "full_name", "mobile", "email", "password"]
# register_args = reqparse.RequestParser()
# for i in register_fields:
#     register_args.add_argument(i, help=f"Please provide {i}", required=True)

# #---------------------LOGIN STORE ADMIN----------------
# login_args = reqparse.RequestParser()
# login_args.add_argument("username", type = str, help = "Please provide usename!", required = True)
# login_args.add_argument("password", type = str, help = "Please provide passowrd", required = True)

# token_args = reqparse.RequestParser()
# token_args.add_argument("token", type = str, help = "Token is missing", required = True)

# #-----------------------STORE ADMIN SIGNUP CLASS----------------------------------
# class RegisterStoreAdmin(Resource):
#     def post(self):
#         args = register_args.parse_args()
#         user = StoreAdmin(**args)

#         try:
#             db.session.add(user)
#             db.session.commit()
#         except Exception as e:
#             return {"message":"Something went wrong", "error": str(e)}, 500
        
#         return {"message":"Sign Up Successful!"}

# #----------------LOGIN RESOURCE------------------------
# class Login_Store_Admin(Resource):
#     def post(self):
#         args = login_args.parse_args()
#         storeradmin = StoreAdmin.query.filter_by(username = args["username"], password = args["password"]).first() 
#         if not storeradmin:
#             return {"message":"Username or Password is wrong"}, 401
#         token = create_token(storeradmin.id)
#         return {"token":token}
    
# #-----------------JWT TOKEN VERIFICATION-------------------        
# class VerifyToken_StoreAdmin(Resource):
#     @token_required
#     def post(self):
#         args = token_args.parse_args()
#         data = jwt.decode(args["token"], secret_token_key, algorithms=['HS256'])
#         storeradmin = StoreAdmin.query.filter_by(id = data['user']).first()
#         return storeradmin.output

# api.add_resource(RegisterStoreAdmin, '/store_admin_signup')
# api.add_resource(Login_Store_Admin, '/store_admin_login')
# api.add_resource(VerifyToken_StoreAdmin, '/verify_token')