from flask import g, request
from flask_restful import Resource, reqparse
from src import db, api
from src.models import Request, User
from src.jwt import token_required

request_args = reqparse.RequestParser()
request_args.add_argument('user_id', type=int, help='User ID is required', required=True)
request_args.add_argument('category_id', type=str, help='Category ID is required', required=False)
request_args.add_argument('category_name', type=str, help='Category Name is required', required=False)
request_args.add_argument('request_type', type=str, help='Request type is required', required=True)
request_args.add_argument('status', type=str, help='User is required', required=True)



class RequestResource(Resource):

    #-----------------GET REQUEST FOR ADMIN--------------------------
    @token_required('admin')
    def get(self):
        request_id = request.args.get("request_id")

        if request_id:
            store_admin_request = Request.query.filter_by(id=request_id).first()
            if store_admin_request:
                return store_admin_request.output
            return {"message": "Request not found!"}

        else:
            store_admin_requests = Request.query.all()
            result = []
            for store_admin_request in store_admin_requests:
                user = User.query.get(store_admin_request.user_id)
                result.append({
                    "id": store_admin_request.id,
                    "user_id":store_admin_request.user_id,
                    "full_name": user.full_name if user else None,
                    "username": user.username if user else None,
                    "category_id": store_admin_request.category_id,
                    "category_name": store_admin_request.category_name,
                    "request_type": store_admin_request.request_type,
                    "status": store_admin_request.status,
                })

            return result


    #------------------------POST REQUEST FOR STORE ADMIN------------------------
    # @token_required
    def post(self):
        try:
            args = request_args.parse_args()

            store_admin_request = Request(**args)
            # print("store_admin_request:", store_admin_request)

            db.session.add(store_admin_request)
            db.session.commit()

            return {"message": "Store admin request submitted successfully"}, 200

        except Exception as e:
            return {"message":"Something went wrong","error": str(e)}, 500
        
    #-----------------APPROVE STORE ADMIN REQUEST--------------------------
    @token_required('admin')
    def put(self):
        try:
            if "request_id" in request.args:
                requestId = request.args.get("request_id")
            else:
                return {"mesasage":"Please provide request id"}

            store_admin_request = Request.query.filter_by(id=requestId).first()

            if not store_admin_request:
                return {"message": "Request not found!"}, 404

            if store_admin_request.request_type.lower() == 'requesting to be store admin' and store_admin_request.status.lower() == 'pending':
                user = User.query.get(store_admin_request.user_id)
                user.role = 'store_admin'
                store_admin_request.status = 'completed'

                db.session.commit()

                return {"message": "Store admin request approved successfully"}, 200
            else:
                return {"message": "Invalid request or request has already been processed"}, 400

        except Exception as e:
            return {"error": str(e)}, 500

    #-----------------REJECT STORE ADMIN REQUEST--------------------------
    @token_required('admin')
    def delete(self):
        try:
            if "request_id" in request.args:
                requestId = request.args.get("request_id")
            else:
                return {"mesasage":"Please provide request id"}
            
            store_admin_request = Request.query.filter_by(id=requestId).first()

            if not store_admin_request:
                return {"message": "Request not found!"}, 404

            if store_admin_request.request_type.lower() == 'requesting to be store admin' and store_admin_request.status.lower() == 'pending':
                store_admin_request.status = 'rejected'
                db.session.commit()

                return {"message": "Store admin request rejected successfully"}, 200
            else:
                return {"message": "Invalid request or request has already been processed"}, 400

        except Exception as e:
            return {"error": str(e)}, 500
        
api.add_resource(RequestResource, '/store_admin_request')
