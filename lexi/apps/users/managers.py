from django.contrib.auth.models import UserManager
from django.conf import settings


class CustomUserManager(UserManager):

    FIELDS = [
        'first_name', 'last_name', 'username', 'email', 'lang'
    ]

    def get_single_api(self, lazy_user):

        user = self.filter(id=lazy_user.id).values(*self.FIELDS)[0]
        if lazy_user.userpic:
        	user['userpic'] = lazy_user.userpic.url
        else:
        	user['userpic'] = None
        return user
