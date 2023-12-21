from flask import Blueprint, jsonify
from flask_restful import Api
from .views import UsersApi, UserApi

users_api = Blueprint("users_api", __name__, url_prefix="/usersapi")
api = Api(users_api)

api.add_resource(UsersApi, "/users")
api.add_resource(UserApi, "/users/<int:id>")
