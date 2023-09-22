import re

from libs.exceptions import BadPasswordException, BadEmailException


def check_password(password: str):
    pattern = r'\d'
    numbers = re.search(pattern, password)
    pattern = r'[A-Z]'
    capital = re.search(pattern, password)
    if numbers and capital and len(password) >= 8:
        return "OK"
    else:
        raise BadPasswordException


def check_email(email: str):
    if "@" in email:
        return "OK"
    else:
        raise BadEmailException

