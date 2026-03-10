import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-api-gateway-secret-key'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'frontend',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'gateway.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'gateway.wsgi.application'

# No database needed for gateway – uses session storage only
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'gateway.sqlite3',
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CORS_ALLOW_ALL_ORIGINS = True

# Microservice URLs
SERVICES = {
    'staff':        os.environ.get('STAFF_SERVICE_URL',        'http://localhost:8001'),
    'manager':      os.environ.get('MANAGER_SERVICE_URL',      'http://localhost:8002'),
    'customer':     os.environ.get('CUSTOMER_SERVICE_URL',     'http://localhost:8003'),
    'catalog':      os.environ.get('CATALOG_SERVICE_URL',      'http://localhost:8004'),
    'book':         os.environ.get('BOOK_SERVICE_URL',         'http://localhost:8005'),
    'cart':         os.environ.get('CART_SERVICE_URL',         'http://localhost:8006'),
    'order':        os.environ.get('ORDER_SERVICE_URL',        'http://localhost:8007'),
    'ship':         os.environ.get('SHIP_SERVICE_URL',         'http://localhost:8008'),
    'pay':          os.environ.get('PAY_SERVICE_URL',          'http://localhost:8009'),
    'comment_rate': os.environ.get('COMMENT_RATE_SERVICE_URL', 'http://localhost:8010'),
    'recommender':  os.environ.get('RECOMMENDER_SERVICE_URL',  'http://localhost:8011'),
}
