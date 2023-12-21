from flask import request
from flask_restful import Resource, abort
from app.users.models import User
from app import db

from app.user_api.schemas.user_schema import UserSchema

class UsersApi(Resource):

    def get(self):
        user_schema = UserSchema(many=True)
        users = User.query.all()
        return {"users": user_schema.dump(users)}

    def post(self):
        schema = UserSchema()
        user_data = schema.load(request.json)
        user = User(**user_data)
        db.session.add(user)
        db.session.commit()

        return {"user": schema.dump(user)}, 201


class UserApi(Resource):
    user_schema = UserSchema(partial=True)

    def get(self, id):
        user = User.query.get_or_404(id)
        if not user:
            abort(404, message="User not found")
        return {"user": self.user_schema.dump(user)}

    def put(self, id):
        user = User.query.get_or_404(id)
        user = self.user_schema.load(request.json, instance=user)

        db.session.commit()

        return {"user": self.user_schema.dump(user)}

    def delete(self, id):
        user = User.query.filter_by(id=id).first_or_404()
        if not user:
            abort(404, message="User not found")
        db.session.delete(user)
        db.session.commit()
        
        return {"message": f"User {user.username} deleted"}