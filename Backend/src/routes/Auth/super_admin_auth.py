# from src import api, db
# from flask_restful import Resource, reqparse
# from src.jwt import token_required, create_token, secret_token_key
# from src.models import SuperAdmin
# import jwt
# import bcrypt  

# login_args = reqparse.RequestParser()
# login_args.add_argument("username", type=str, help="Please provide username!", required=True)
# login_args.add_argument("password", type=str, help="Please provide password", required=True)

# token_args = reqparse.RequestParser()
# token_args.add_argument("token", type=str, help="Token is missing", required=True)

# class LoginSuperAdmin(Resource):
#     def post(self):
#         args = login_args.parse_args()
#         # superadmin = SuperAdmin.query.filter_by(username=args["username"]).first()
#         superadmin = SuperAdmin.query.filter_by(username = args['username'], password = args['password']).first()
        
#         if superadmin:  #and superadmin.password
#             # if "super admin" in [role.name for role in superadmin.roles]:
#             token = create_token(superadmin.id)
#             return {"token": token}
        
#         return {"message": "Invalid username or password"}, 401

# class VerifyTokenSuperAdmin(Resource):
#     @token_required
#     def post(self):
#         args = token_args.parse_args()
#         data = jwt.decode(args["token"], secret_token_key, algorithms=['HS256'])
#         superadmin = SuperAdmin.query.filter_by(id=data['user']).first()

#         if not superadmin:
#             return {"message": "Super admin not found"}, 404

#         return superadmin.output

# api.add_resource(LoginSuperAdmin, '/admin_login')
# api.add_resource(VerifyTokenSuperAdmin, '/verify_token')
