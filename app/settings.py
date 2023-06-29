from os import environ
import logging

INFO_LOGGING_FORMAT = 'INFO:     %(asctime)s %(message)s'
WARNING_LOGGING_FORMAT = 'WARNING:     %(asctime)s %(message)s'

MANDATORY_ENV_VARS = ['SECRET_KEY', 
                      'DATABASE_URL', 
                      'SUPERUSER_EMAIL', 
                      'SUPERUSER_PASSWORD']

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