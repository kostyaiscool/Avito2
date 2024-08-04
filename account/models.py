import datetime

import jwt
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
class UserManager(BaseUserManager):
    def create_user(self, email=None, number=None, password=None, **extra_fields):
        if not email and not number:
            raise ValueError(_('Users must have either email or phone number'))

        if email:
            email = self.normalize_email(email)

        user = self.model(email=email, number=number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True'))

        return self.create_user(email, number, password, **extra_fields)

class Ach(models.Model):
    name = models.CharField(_('Achname'), max_length=50, blank=False, null=False)
    description = models.CharField(_('Description'), max_length=200, blank=True, null=True)
    icon = models.ImageField(null=False, blank=False, upload_to='achicons')
    reward = models.IntegerField(null=False, blank=False)
    difficulty = models.IntegerField(null=True, blank=True, default=5)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('Email address'), unique=True, null=False, blank=False)
    number = PhoneNumberField(_('Phone number'), unique=True, null=True, blank=True, max_length=20)
    name = models.CharField(_('Username'), max_length=30, unique=False, blank=False, null=False)
    avatar = models.ImageField(default='default.png', upload_to='icons')
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)

    is_email_confirmed = models.BooleanField(
        default=False,
    )
    is_phone_confirmed = models.BooleanField(
        default=False,
    )
    is_email_2fa_enabled = models.BooleanField(
        default=False,
    )
    is_phone_2fa_enabled = models.BooleanField(
        default=False,
    )
    achs = models.ManyToManyField(blank=True, to=Ach)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['number']

class ActiveSession(models.Model):
    class Meta:
        verbose_name = _("Active Session")
        verbose_name_plural = _("Active Sessions")

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text=_('The user associated with this active session.')
    )
    token = models.CharField(
        max_length=255,
        help_text=_('The token used for the session.')
    )
    date = models.DateTimeField(
        auto_now_add=True,
        help_text=_('The date and time when the session was created.')
    )
    is_online = models.BooleanField(
        _("online"),
        default=False,
        help_text=_("Is user online via this session.")
    )

    def save(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().save(*args, **kwargs)

        if request:
            session_key = request.session.session_key
            if not session_key:
                request.session.save()
                session_key = request.session.session_key

                self.session_key = session_key
                super().save(update_fields=['session_key'])


    def is_active(self):
        try:
            decoded = jwt.decode(self.token, settings.SECRET_KEY, algorithms=["HS256"])
            expire = datetime.fromtimestamp(decoded['exp'])
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False
        return datetime.utcnow() < expire
