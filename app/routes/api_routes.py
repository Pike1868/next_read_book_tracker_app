from flask_restful import Api, Resource, reqparse
from ..models import User, db
from sqlalchemy.exc import IntegrityError
from flask_login import login_user

api = Api()

parser = reqparse.RequestParser()
parser.add_argument('username', type=str, required=True,
                    help="Username cannot be blank!")
parser.add_argument('password', type=str, required=True,
                    help="Password cannot be blank!")
parser.add_argument('email', type=str, required=True,
                    help="Email cannot be blank!")


class RegisterResource(Resource):
    def post(self):
        args = parser.parse_args()
        username = args.get('username')
        password = args.get('password')
        email = args.get('email')

        existing_username = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email=email).first()

        if existing_username:
            return {'error': "Username is taken, please pick another."}, 400
        if existing_email:
            return {'error': "Email is already registered, please try logging in."}

        new_user = User(username=username, password=password, email=email)
        db.session.add(new_user)
        try:
            db.session.commit()
            login_user(new_user)
        except IntegrityError:
            return {"error": "Error in adding the user."}, 500

        return {"message": "Welcome! Successfully Created Your Account!"}, 200


api.add_resource(RegisterResource, '/register')
