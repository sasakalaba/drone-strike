import os
from .env import ENV_BOOL, ENV_LIST, ENV_SETTING, ABS_PATH, ENV_STR
import dj_database_url


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUG = ENV_BOOL('DEBUG', False)
ALLOWED_HOSTS = ENV_LIST('ALLOWED_HOSTS', ',', ['*'] if DEBUG else [])
SECRET_KEY = ENV_STR('SECRET_KEY', 'secret' if DEBUG else '')


# Application definition
INSTALLED_APPS = [
    'strike.apps.StrikeConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            ABS_PATH('templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

ROOT_URLCONF = 'project.urls'
WSGI_APPLICATION = 'project.wsgi.application'
DATABASES = {'default': dj_database_url.config()}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'


# Static files (CSS, JavaScript, Images)
STATIC_URL = ENV_STR('STATIC_URL', '/static/')
STATIC_ROOT = ENV_STR('STATIC_ROOT', ABS_PATH('static'))
STATICFILES_DIRS = (
    ABS_PATH('project', 'static'),
)

# Strike configuration
STRIKE_DATA_URL = ENV_STR('STRIKE_DATA_URL', 'https://api.dronestre.am/data')
