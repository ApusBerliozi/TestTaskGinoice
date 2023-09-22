import json
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import request, abort
from flask import current_app as app

from libs.authorization import check_token
from libs.exceptions import BadPasswordException, BadEmailException
from . import CreateUserRequest, CreateTokenRequest, GetUserResponse
from .entities import User
from .models import create_user, check_user, add_token, get_user


@app.route("/sign_up/", methods=["POST"])
def sign_up():
    """Create new user.
        ---
        post:
          description: Creates a new user.
          requestBody:
            content:
              application/json:
                schema: CreateUserRequest

            responses:
                200:
                  content:
                    application/json:
                      schema:
                        user_id:
                            type: number
                        signature:
                            type: string
                400:
    """

    user_info = User(**request.json)
    try:
        user_info.validate_new_user()
    except BadPasswordException:
        abort(400, description="Your password is not safe. Please notice that a safe one includes at least 1 number, "
                               "a capital letter, and contains 8 characters or more.")
    except BadEmailException:
        abort(400, description="Your email is not correct.")
    return create_user(user_info=user_info)


@app.route("/sign_in/", methods=["POST"])
def sign_in():
    """Create new user.
        ---
        post:
          description: Create token for user
          requestBody:
            content:
              application/json:
                schema: CreateTokenRequest
            200:
              content:
                application/json:
                  schema:
                    auth_token:
                      type: string
            403:
    """
    user_info = User(**request.json)
    user_info = check_user(email=user_info.email,
                           password=user_info.password)
    if user_info:
        return add_token(user_id=user_info.id,
                         user_name=user_info.name)
    abort(403, description="Either your password or login isn't correct")


@app.route("/user/", methods=["GET"])
def user_endpoint():
    """Get user info.
        ---
        get:
          responses:
            200:
              content:
                application/json:
                  schema: GetUserResponse
    """
    token = check_token(request=request)
    user_info = get_user(token=token)
    if user_info:
        return {
            "name": user_info.name,
            "surname": user_info.surname,
            "email": user_info.email,
            "eth_address": user_info.eth_address
        }
    abort(403, description="You are not authorized to access this resource.")


#Тут вцелом можно было и не выносить в функцию, но мне показалось что код будет выглядетть аккуратней
def create_specification():
    spec = APISpec(
        title="My API",
        version="1.0.0",
        openapi_version="3.0.2",
        plugins=[FlaskPlugin(), MarshmallowPlugin()],
    )

    spec.components.schema("CreateUserRequest", schema=CreateUserRequest)
    spec.components.schema("CreateTokenRequest", schema=CreateTokenRequest)
    spec.components.schema("GetUserResponse", schema=GetUserResponse)
    with app.test_request_context():
        spec.path(view=sign_up)
        spec.path(view=sign_in)
        spec.path(view=user_endpoint)
    return spec


open_api_document = create_specification()


@app.route("/api/spec", methods=["GET"])
def api_spec():
    return json.dumps(open_api_document.to_dict())

