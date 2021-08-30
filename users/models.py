import jwt

from datetime import datetime, timedelta

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings


class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None, **kwargs):
        """ Create and return user with username, email, password, etc """
        if not username:
            raise TypeError('Users must have a unique username.')
        if not email:
            raise TypeError('Users must have a unique email address.')
        if not password:
            raise TypeError('Users must have a password.')

        user = self.model(username=username, email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        """ Create and return superuser """
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractUser):
    email = models.EmailField(verbose_name='email address', unique=True)
    image = models.ImageField(default='profile_pics/user_default.png', upload_to='profile_pics')

    objects = UserManager()

    def get_absolute_url(self):
        return reverse('users:profile-user', kwargs={'pk': self.id})

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """ Generates a JWT-token that stores users ID. The token validity period is 1 day from creation."""
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token


