from uuid import uuid4
from .base import *

DEBUG = True
SECRET_KEY = uuid4().hex

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)
