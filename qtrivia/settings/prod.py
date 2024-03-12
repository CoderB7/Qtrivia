from .base import *

DEBUG = False

ADMINS = [
    ('redmi', 'iutstudent2022@gmail.com')
]

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'qtrivia_db',
        'USER': 'qtrivia',
        'PASSWORD': 'qwerty',
    }
}
