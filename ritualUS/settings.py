"""
Django settings for ritualUS project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
import environ
from pathlib import Path
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, '.env'))
runRemote = True
if runRemote:
    SECRET_KEY = env('RITUALUS_KEY')
else:
    SECRET_kEY = ''

STRIPE_API_KEY = 'sk_test_51QOizQL6pSx3PYtRvOotv226hmJhjzsKqS7RRHl5wBSUH3kTY5hygQgbLt2ziJc1DYTNoiylV3kA0qgl6XrbJV9H00Gh7VsP51'  # clave secreta
STRIPE_PUBLISHABLE_KEY = 'pk_test_51QOizQL6pSx3PYtRJV56TkRpmAfMEavBeyuwZMEZZ6iZqLxp1Ef797WPBr7J1HQc5JDw62dZbElmR6T5INXN8mt100cpgCfCyM'  # clave pública


ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-3qng-%*rfl!(*3(6_a0c@g=g+-99wu@++)10$d4fl)@gf2%c!z'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/


ALLOWED_HOSTS = ['0.0.0.0', 'localhost', '127.0.0.1', 'ritualUSApp.pythonanywhere.com', 'www.ritualUSApp.pythonanywhere.com']
AUTH_USER_MODEL = 'ritualUS.CustomUser'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'allauth',
    'allauth.account',
    'ritualUS'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = (
    # Backend de autenticación predeterminado de Django
    'django.contrib.auth.backends.ModelBackend',
    # Backend de autenticación de allauth
    'allauth.account.auth_backends.AuthenticationBackend',
)

ROOT_URLCONF = 'ritualUS.urls'

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
        },
    },
]


WSGI_APPLICATION = 'ritualUS.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
    }
}

if ENVIRONMENT == 'production':
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    SESSION_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_REDIRECT_EXEMPT = []
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


ACCOUNT_FORMS = {
    'signup': 'ritualUS.forms.CustomSignupForm',
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'ritualUS/static']
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SITE_ID = 1
LOGIN_REDIRECT_URL = '/'  # Redirección después de iniciar sesión
LOGOUT_REDIRECT_URL = '/'
ACCOUNT_EMAIL_REQUIRED = True  # Requiere un correo electrónico para el registro
# Opcional: 'mandatory' o 'none' según prefieras
ACCOUNT_EMAIL_VERIFICATION = 'optional'
CRISPY_TEMPLATE_PACK = 'bootstrap4'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
