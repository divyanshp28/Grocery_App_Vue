from src import api, db
from flask_restful import Resource, reqparse
from src.jwt import token_required, create_token, secret_token_key
from src.models import User
import jwt

#-------------------USER SIGNUP-----------------------------------------
register_fields = ["username", "full_name", "mobile", "email", "password"]
register_args = reqparse.RequestParser()
for i in register_fields:
    register_args.add_argument(i, help=f"Please provide {i}", required=True)


#-------------------USER LOGIN------------------------------------------
login_args = reqparse.RequestParser()
login_args.add_argument("username", type = str, help = "Please provide usename!", required = True)
login_args.add_argument("password", type = str, help = "Please provide passowrd", required = True)

token_args = reqparse.RequestParser()
token_args.add_argument("token", type = str, help = "Token is missing", required = True)

#-----------------------USER REGISTER CLASS----------------------------------
class RegisterUser(Resource):
    def post(self):
        args = register_args.parse_args()
        user = User(**args)

        try:
            # ASSIGNING ROLE
            user.role = "user"
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            return {"message":"Something went wrong", "error": str(e)}, 500
        
        return {"message":"Sign Up Successful!"}
    
#-----------------------USER LOGIN CLASS-----------------------------------
class Login_user(Resource):
    def post(self):
        args = login_args.parse_args()
        user = User.query.filter_by(username = args["username"], password = args["password"]).first() 
        if not user:
            return {"message":"Username or Password is wrong"}, 401
        token = create_token(user.id, user.role)
        return {"user_id": user.id, "username":user.username, "role":user.role, "token":token}
    
#-----------------------JWT TOKEN VERIFICATION-----------------------------    
class VerifyToken(Resource):
    # @token_required
    def post(self):
        args = token_args.parse_args()
        data = jwt.decode(args["token"], secret_token_key, algorithms=['HS256'])
        user = User.query.filter_by(id = data['user_id']).first()
        return user.output
    
api.add_resource(RegisterUser, '/signup')
api.add_resource(Login_user, '/login')
api.add_resource(VerifyToken, '/verify_token')