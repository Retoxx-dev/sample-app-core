from os import environ

MANDATORY_ENV_VARS = ['SECRET_KEY', 
                      'DATABASE_URL', 
                      'SUPERUSER_EMAIL', 
                      'SUPERUSER_PASSWORD']

for var in MANDATORY_ENV_VARS:
    if var not in environ:
        raise ValueError(f'{var} environment variable is not set')

SECRET_KEY = environ.get('SECRET_KEY')
DATABASE_URL = environ.get('DATABASE_URL')

SUPERUSER_EMAIL = environ.get('SUPERUSER_EMAIL')
SUPERUSER_PASSWORD = environ.get('SUPERUSER_PASSWORD')
