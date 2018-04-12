from uuid import uuid4
from .base import *

DEBUG = True
SECRET_KEY = uuid4().hex
STRIKE_DATE_MONTH_RANGE = 3

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)
