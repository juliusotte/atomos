import os
import string
import random


def env(variable: str, default: object):
    return os.environ.get(variable, default)


# Default application name.
_default_name = 'atomos'

# Default host for application execution.
# Using development, the default is usually 'localhost'.
_default_host = 'localhost'

# Environment indicating the stage of deployment.
ENVIRONMENT = env('ENVIRONMENT', 'development')

# Application name
APP_NAME = env('APP_NAME', _default_name)

# Database
DB_HOST = env('DB_HOST', _default_host)
DB_PORT = env('DB_PORT', 5432)
DB_USER = env('DB_USER', APP_NAME)
DB_PASSWORD = env('DB_PASSWORD', APP_NAME)
DB_NAME = env('DB_NAME', APP_NAME)
DB_DRIVER = env('DB_DRIVER', 'postgresql')
DB_URI = f'{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Redis
REDIS_HOST = env('REDIS_HOST', _default_host)
REDIS_PORT = env('REDIS_PORT', 6379)

# SMTP
SMTP_HOST = env('SMTP_HOST', _default_host)
SMTP_PORT = env('SMTP_PORT', 11025)
SMTP_USER = env('SMTP_USER', 'bot@localhost')
SMTP_PASSWORD = env('SMTP_PASSWORD', '')

# API
API_HOST = env('API_HOST', _default_host)
API_PORT = env('API_PORT', 50051)

# Secret
SECRET_KEY = env('SECRET_KEY', ''.join(random.choices(string.digits + string.ascii_letters, k=50)))
