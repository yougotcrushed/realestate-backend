import os
import dj_database_url
from .common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['realestate-prod-fdf77c6bb00a.herokuapp.com']

SECRET_KEY = os.environ['SECRET_KEY']

DATABASES = dj_database_url.config()
