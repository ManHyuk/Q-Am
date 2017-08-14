import os
from .common import *

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS += ['storages']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'qam-postgrsql.cb0uke8glomz.ap-northeast-2.rds.amazonaws.com',
        'NAME': 'qam_postgresql',
        'USER': 'qam',
        'PASSWORD': 'jkjkqam123',
    },
}

DATABASE_OPTIONS = {'charset': 'utf8'}

STATICFILES_STORAGE = 'qam.storages.StaticS3Boto3Storage'
DEFAULT_FILE_STORAGE = 'qam.storages.MediaS3Boto3Storage'

AWS_ACCESS_KEY_ID = 'AKIAJPOFB3RQZTTCQDDA'  # IAM admin-user
AWS_SECRET_ACCESS_KEY = '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'

AWS_REGION = 'ap-northeast-2'
AWS_STORAGE_BUCKET_NAME = 'qam-static-or-media'

AWS_QUERYSTRING_AUTH = False

STATIC_URL = '/static/'

