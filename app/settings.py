from os import environ
import logging

INFO_LOGGING_FORMAT = 'INFO:     %(asctime)s %(message)s'
WARNING_LOGGING_FORMAT = 'WARNING:     %(asctime)s %(message)s'

MANDATORY_ENV_VARS = ['SECRET_KEY',
                      'DATABASE_URL',
                      'SUPERUSER_EMAIL',
                      'SUPERUSER_PASSWORD',
                      'RABBITMQ_CONNECTION_STRING',
                      'RABBITMQ_QUEUE_NAME'
                      ]


def check_env_vars():
    for var in MANDATORY_ENV_VARS:
        if var not in environ:
            raise ValueError(f'{var} environment variable is not set')


def configure_logging():
    ENV = environ.get('ENV', 'development')
    if ENV == 'production':
        logging.basicConfig(level=logging.INFO, format=WARNING_LOGGING_FORMAT)
        logging.info('Running in production mode')
    if ENV == 'development':
        logging.basicConfig(level=logging.INFO, format=INFO_LOGGING_FORMAT)
        logging.info('Running in development mode')


SECRET_KEY = environ.get('SECRET_KEY')
DATABASE_URL = environ.get('DATABASE_URL')
SUPERUSER_EMAIL = environ.get('SUPERUSER_EMAIL')
SUPERUSER_PASSWORD = environ.get('SUPERUSER_PASSWORD')

RABBITMQ_CONNECTION_STRING = environ.get('RABBITMQ_CONNECTION_STRING')
RABBITMQ_QUEUE_NAME = environ.get('RABBITMQ_QUEUE_NAME')

CORS_ORIGINS = environ.get('CORS_ORIGINS')

STORAGE_ACCOUNT_URL = environ.get('STORAGE_ACCOUNT_URL')
STORAGE_ACCOUNT_ACCESS_KEY = environ.get('STORAGE_ACCOUNT_ACCESS_KEY')
