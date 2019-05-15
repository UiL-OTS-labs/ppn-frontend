from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.db import models

from api.auth.exceptions import AccountAlreadyExistsException
from api.resources.account_resources import UserCreationData


class RemoteApiUserManager(BaseUserManager):

    def get_by_email(self, email: str, stop_recursion: bool = False):
        email = email.strip()

        try:
            user = self.get(email=email)
        except RemoteApiUser.DoesNotExist:
            # Fix the annoying problem that the university allows students
            # to have 2 emails
            if not stop_recursion and email.endswith('@students.uu.nl'):
                email = email.replace('students.uu.nl', 'uu.nl')
                user = self.get_by_email(email, True)
            elif not stop_recursion and email.endswith('@uu.nl'):
                email = email.replace('uu.nl', 'students.uu.nl')
                user = self.get_by_email(email, True)
            else:
                user = None

        return user

    def create_user(self,
                    email: str,
                    name: str,
                    multilingual: bool = None,
                    language: str = None,
                    dyslexic: bool = None,
                    mailing_list: bool = False,
                    password: str = None):

        resource = UserCreationData(
            email=email,
            name=name,
            multilingual=multilingual,
            language=language,
            dyslexic=dyslexic,
            mailing_list=mailing_list,
            password=password,
        )

        response = resource.put()

        if response.message and response.message != 'OK':
            if response.message == 'ACCOUNT_ALREADY_EXISTS':
                raise AccountAlreadyExistsException

    def create_superuser(self, *args, **kwargs):
        raise RuntimeError("Admin User generation is not supported in this "
                           "application. Create users in the backend!")


class RemoteApiUser(PermissionsMixin, AbstractBaseUser):
    objects = RemoteApiUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    email = models.EmailField(unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    is_ldap_account = models.BooleanField(default=False)

    @property
    def is_leader(self) -> bool:
        return self.groups.filter(name=settings.GROUPS_LEADER).exists()

    @property
    def is_participant(self) -> bool:
        return self.groups.filter(name=settings.GROUPS_PARTICIPANT).exists()

    def __str__(self):
        return self.get_username()
