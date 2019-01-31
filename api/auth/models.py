from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.conf import settings


class RemoteApiUserManager(BaseUserManager):

    # TODO: create API calls to handle this

    def create_user(self, *args, **kwargs):
        raise RuntimeError("User generation is not supported in this application. Create users in the backend!")

    def create_superuser(self, *args, **kwargs):
        raise RuntimeError("User generation is not supported in this application. Create users in the backend!")


class RemoteApiUser(PermissionsMixin, AbstractBaseUser):

    objects = RemoteApiUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    email = models.EmailField(unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    @property
    def is_leader(self) -> bool:
        return self.groups.filter(name=settings.GROUPS_LEADER).exists()

    @property
    def is_participant(self) -> bool:
        return self.groups.filter(name=settings.GROUPS_PARTICIPANT).exists()

    def __str__(self):
        return self.get_username()
