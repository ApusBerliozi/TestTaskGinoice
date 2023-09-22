from datetime import datetime

from libs.crypto import generate_signature
from libs.authorization import generate_token
from . import db
from .entities import User
from flask import current_app as app


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)


class UserModel(BaseModel):
    __tablename__ = "user"

    name = db.Column(db.VARCHAR(255), nullable=False)
    surname = db.Column(db.VARCHAR(255), nullable=False)
    email = db.Column(db.VARCHAR(255), unique=True, nullable=False)
    eth_address = db.Column(db.VARCHAR(255), nullable=False)
    password = db.Column(db.VARCHAR(255), nullable=False)
    auth_token = db.Column(db.VARCHAR(255), nullable=True)


def create_user(user_info: User):
    db.session.begin()
    user = UserModel(name=user_info.name,
                     surname=user_info.surname,
                     email=user_info.email,
                     eth_address=user_info.eth_address,
                     password=user_info.password)
    db.session.add(user)
    db.session.commit()
    return {
        "user_id": user.id,
        "signature": generate_signature(user_id=user.id,
                                        private_key=app.config["ETHEREUM_PRIVATE_KEY"]).hex()
    }


def check_user(email: str,
               password: str):
    user = UserModel.query.filter_by(email=email,
                                     password=password).first()
    return user


def add_token(user_id: int,
              user_name: str):
    token = generate_token(user_id=user_id,
                           name=user_name)
    user = UserModel.query.get(user_id)
    user.auth_token = token
    db.session.commit()
    return {"auth_token": token}


def get_user(token: str):
    user = UserModel.query.filter_by(auth_token=token).first()
    return user
