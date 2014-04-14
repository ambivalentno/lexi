import os

from .base import *
from .utils import *
from .users import *

SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = os.environ.get('DEBUG') or False

INSTALLED_APPS += (
    'downtime',
)

MIDDLEWARE_CLASSES = (
     'downtime.middleware.DowntimeMiddleware',
) + MIDDLEWARE_CLASSES

MAINTENANCE_FILE = root('../etc/maintenance')

DOWNTIME_EXEMPT_PATHS = (
    '/admin',
    '/static',
)
