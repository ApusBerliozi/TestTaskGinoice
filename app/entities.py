from dataclasses import dataclass

from libs.validators import check_password, check_email


@dataclass
class User:
    name: str = None
    surname: str = None
    email: str = None
    eth_address: str = None
    password: str = None
    token: str = None

    def validate_new_user(self):
        check_password(self.password)
        check_email(self.email)
