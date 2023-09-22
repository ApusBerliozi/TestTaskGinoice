import datetime
import jwt
from flask import abort
from flask import current_app as app


def generate_token(user_id: int,
                   name: str):
    payload = {
        'user_id': user_id,
        'name': name,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)  # Token expiration time
    }

    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token


def check_token(request):
    authorization_header = request.headers.get('Authorization')
    if authorization_header:
        token_parts = authorization_header.split()
        if len(token_parts) == 2 and token_parts[0].lower() == 'bearer':
            token = token_parts[1]
            return token
        else:
            abort(401)
