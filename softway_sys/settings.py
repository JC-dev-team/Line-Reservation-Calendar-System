"""
Django settings for softway_sys project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd91v90b$q&w!9x6wn5_iaej@a%^wj#v!!b(*%+h@$pj8e6=gz='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'main',
    'booking',
    'userdashboard',
    'admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
]
# Invisible reCaptcha
RECAPTCHA_PUBLIC_KEY = '6LdG38MUAAAAAHVni33TLj3b27-gCC5X1-foxhQO'
RECAPTCHA_PRIVATE_KEY = '6LdG38MUAAAAAIX4_sTGovEK81Wa15798opihJ9n'

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django_session_timeout.middleware.SessionTimeoutMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
# Session timeout using package
# SESSION_EXPIRE_SECONDS = 3600
# SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True

# Security settings
SECURE_CONTENT_TYPE_NOSNIFF = True
CSRF_COOKIE_SECURE = False  # need to be True when production
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = False  # need to be True when production
X_FRAME_OPTIONS = 'DENY'  # default = 'SAMEORIGIN'
# SECURE_HSTS_SECONDS = 31536000 # need to be uncomment when production
SECURE_HSTS_INCLUDE_SUBDOMAINS = False  # need to be True when production
SECURE_HSTS_PRELOAD = False  # need to be True when production
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https') # need to be uncomment when production

# Authentication
AUTH_USER_MODEL = 'main.Staff'
AUTHENTICATION_BACKENDS = ['common.utility.auth.ClientAuthBackend',
                           'common.utility.auth.StaffAuthBackend',
                           'django.contrib.auth.backends.ModelBackend',
                           ]

# session options
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_SECURE = False  # when deploy need to set to True
# SESSION_SAVE_EVERY_REQUEST=True
# SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 60*15

# linebot keys for user
LINE_CHANNEL_ACCESS_TOKEN_USER = "hVTaUoLcsdGG+pGoBTcAXG8OB41nU9YLxb3SeQiCi9leMxE50U2BaW9dFfIcf0wAvIQpW080FGL6efM545aq7tfEZMNffOIJZBFl0pFglvq71onAm6Wfy7tdX8c696QrrPSgZB+uePfe1b+9+swpElGUYhWQfeY8sLGRXgo3xvw="

# linebot keys for admin
LINE_CHANNEL_ACCESS_TOKEN_ADMIN = "kizgP14pi0bH/Mm4fGvjCwrriOj8sOvAZrKOrIoVbh41ryKDT8manl2AnguR0fV76q4UQiBbo0e1l8e4x2GUCeH6cFTRlP08260WALo9fRFA5Pm7o6nT9RljC6QXw9bX91AghNxBKgZlMSV3fBsGYQdB04t89/1O/w1cDnyilFU="

ROOT_URLCONF = 'softway_sys.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries':{
                'tagfunctions': 'templates.templatetags.tagfunctions',
            }
        },
    },
]

WSGI_APPLICATION = 'softway_sys.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# You need to downgrade openssl by conda install openssl=1.0.2r
# when you are using macOS

# Deploy on aws elastic beanstalk
# if 'RDS_HOSTNAME' in os.environ:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.mysql',
#             'NAME': os.environ['RDS_DB_NAME'],
#             'USER': os.environ['RDS_USERNAME'],
#             'PASSWORD': os.environ['RDS_PASSWORD'],
#             'HOST': os.environ['RDS_HOSTNAME'],
#             'PORT': os.environ['RDS_PORT'],
#         }
#     }
# else:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'softway',
        'USER': 'root',
        'PASSWORD': 'rootadmin',
        'HOST': 'mysqlbeenattack.cbelqfilciuy.us-east-1.rds.amazonaws.com',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'zh-Hant'

TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'staticfiles'),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',

)

# Email Setttings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'softwayliving@gmail.com'
EMAIL_HOST_PASSWORD = 'mzrmfbgxebtwmlvc'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
