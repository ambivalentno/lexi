import re

from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.conf import settings

from django.utils.translation import ugettext as _
from django.core import validators
from django.utils.http import urlquote
from django.utils import timezone

from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

from core.utils.thumbs import ImageWithThumbsField
from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Model auth/customizing.
    """
    username = models.CharField(
        _('username'), max_length=255, unique=True,
        help_text=_('Required. 255 characters or fewer. Letters, numbers and '
                    '@/./+/-/_ characters'),
        validators=[
            validators.RegexValidator(
                re.compile('^[\w.@+-]+$'),
                _('Enter a valid username.'), 'invalid'
            )
        ]
    )
    first_name = models.CharField(_('first name'), max_length=255, blank=True)
    last_name = models.CharField(_('last name'), max_length=255, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(
        _('staff status'), default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'
        )
    )
    is_teacher = models.BooleanField(
        _('teacher status'), default=False,
        help_text=_(
            'Designates whether the user can create new courses.'
        )
    )
    is_active = models.BooleanField(
        _('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.')
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    lang = models.CharField(_('Language'),
                            max_length=3,
                            choices=settings.LANGUAGES,
                            blank=True)

    userpic = ImageWithThumbsField(_('User picture'),
                                   upload_to='userpic_images/',
                                   sizes=settings.USERPIC_SIZES,
                                   null=True, blank=True
                                   )

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.username)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)


@receiver(pre_delete, sender=User)
def userpic_pre_delete(sender, instance, **kwargs):
    """Delete userpics"""

    image = instance.userpic
    if image:
        try:
            image.storage.delete(image.name)
        except:
            pass
