import os
import json
import pymysql
from django.core.exceptions import ImproperlyConfigured
from pathlib import Path
from datetime import timedelta

pymysql.install_as_MySQLdb()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Read secrets.json file
SECRET_DIR = os.path.join(BASE_DIR, 'secrets.json')
with open(SECRET_DIR, 'r') as f: 
    secrets = json.loads(f.read())
    
def get_secret(setting, secrets=secrets): 
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

SECRET_KEY = get_secret("SECRET_KEY")
ALGORITHM = get_secret("ALGORITHM")

DEBUG = False 
ALLOWED_HOSTS = ["*"] # server domain or IP, localhost


# Application definition

INSTALLED_APPS = [
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'storages',
    'users',
    'files',
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

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=6),      
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),    
    'ROTATE_REFRESH_TOKENS': True,                 
    'BLACKLIST_AFTER_ROTATION': True,              
    'UPDATE_LAST_LOGIN': False,                     
    'ALGORITHM': ALGORITHM,                           
    'SIGNING_KEY': SECRET_KEY,              
    'VERIFYING_KEY': None,                         
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,
    'AUTH_HEADER_TYPES': ('Bearer',),               
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',        
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}

ROOT_URLCONF = 'pghj_server.urls' # ????????? URL
AUTH_USER_MODEL = 'users.User'    # ?????? ????????? ??????

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'pghj_server.wsgi.application'

# Databases
# https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-DATABASES

DATABASES = get_secret("DATABASES")
DATABASE_OPTIONS = {"charset": "utf8"}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# PPTX template file path
TEMPLATE_DIR = os.path.join(BASE_DIR, 'files/templates/')

# Media(image, pptx) file path
MEDIA_DIR = os.path.join(BASE_DIR, 'files/')

# AWS S3 options
AWS_ACCESS_KEY_ID = get_secret("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = get_secret("AWS_SECRET_ACCESS_KEY")
BUCKET_NAME = get_secret("BUCKET_NAME")
S3_DIR = "https://s3.ap-northeast-2.amazonaws.com/" + BUCKET_NAME + "/"