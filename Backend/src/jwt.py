import jwt
from functools import wraps
from flask_restful import reqparse
from datetime import datetime, timedelta
from flask import request, g

secret_token_key = 'kjfcbakhvdjagvdlsglsjbfkhsbvwet38*^&&t-t754398y5r'

def token_required(required_role):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            g.user = None
            
            if 'token' in request.headers:
                token = request.headers['token']
                # print('Received Token:', token)

            else:
                return {"message": "Not Authorized"}, 401

            if "role" in request.headers:
                role = request.headers['role']

            else:
                return {"message": "User role not found"}, 401

            try:
                data = jwt.decode(token, secret_token_key, algorithms=['HS256'])
                user_role = data.get('role', 'user')

                if user_role != required_role:
                    return {"message": "Insufficient permissions"}, 403
                
                #  STORING USER DATA IN G
                # g.user = data
                g.user = {'user_id': data.get('user_id'), 'role': role}

            except:
                return {"message": "Invalid Token!"}, 401

            return f(*args, **kwargs)

        return decorated

    return decorator

#-----------------------------CREATING TOKEN---------------------------------------

def create_token(id, role):
    token = jwt.encode({
        "user_id":id,
        "role": role,
        "exp":datetime.utcnow() + timedelta(minutes = 30)   #token valid for 30 mins
    }, secret_token_key, algorithm="HS256")
    return token

