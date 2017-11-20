from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8fj$l6qcm&2-!-$8*0-pp$1l)o)*h+n6etzwn7+-$-7_^h%=6*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1']
STATIC_ROOT = os.path.join(BASE_DIR, 'assets')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

SMSC_LOGIN = 'TheGoshikus'
SMSC_PASSWORD = 'TheGoshikus1991'

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = 'mails' # change this to a proper location

EMAIL_FROM = 'robot@inkoro.ru'
EMAIL_FOR_ORDERS = 'zakupki@food-prod.ru'