AUTH_USER_MODEL = 'users.User'

USERPIC_SIZES = (
    (100, 100),
    (50, 50),
)

# django-social-auth
SOCIAL_AUTH_USER_MODEL = 'users.User'
SOCIAL_AUTH_DEFAULT_USERNAME = 'new_social_auth_user'

SOCIAL_AUTH_RAISE_EXCEPTIONS = False
FACEBOOK_EXTENDED_PERMISSIONS = ['email']

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.google.GoogleOAuth2Backend',
    'social_auth.backends.OpenIDBackend',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_PIPELINE = (
    'social_auth.backends.pipeline.social.social_auth_user',
    'social_auth.backends.pipeline.associate.associate_by_email',
    'social_auth.backends.pipeline.user.get_username',
    'social_auth.backends.pipeline.user.create_user',
    'social_auth.backends.pipeline.social.associate_user',
    'social_auth.backends.pipeline.social.load_extra_data',
    'social_auth.backends.pipeline.user.update_user_details',
    'users.avatars.save_user_pic',
)

SOCIAL_AUTH_UID_LENGTH = 222
SOCIAL_AUTH_NONCE_SERVER_URL_LENGTH = 200
SOCIAL_AUTH_ASSOCIATION_SERVER_URL_LENGTH = 135
SOCIAL_AUTH_ASSOCIATION_HANDLE_LENGTH = 125

GOOGLE_OAUTH2_USE_UNIQUE_USER_ID = True
FACEBOOK_EXTENDED_PERMISSIONS = ['email', ]
#FACEBOOK_EXTRA_DATA = ['username']

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/'
LOGIN_ERROR_URL = '/login_error/'
