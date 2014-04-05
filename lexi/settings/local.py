# Make this unique, and don't share it with anybody.
SECRET_KEY = ')!!0w02d99_%te8+y4r*pke=p3eykxy29-y=wum@pc+se&amp;-5%i'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'lexi',
        'USER': 'lexi',
        'PASSWORD': '',
        'PORT': '',
        'HOST': 'localhost',
    },
}

import sys
if 'test' in sys.argv or 'test_coverage' in sys.argv: #Covers regular testing and django-coverage
    DATABASES['default']['engine'] = 'django.db.backends.sqlite3'

SOUTH_TESTS_MIGRATE = False
