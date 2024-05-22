import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

SECRET_KEY = '*+uid(@$^dg8)1bs)*aasdsgfhsdas3aaea(0_=n@c6*xtaasdsumo'

DEBUG = False

ALLOWED_HOSTS = ['go-menu.kz', '185.22.64.19']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'gositedb',
        'USER': 'medet',
        'PASSWORD': 'dostar1996',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

ROOT_URLCONF = 'gosite.urls'

STATIC_ROOT =  os.path.join(BASE_DIR, 'static')
