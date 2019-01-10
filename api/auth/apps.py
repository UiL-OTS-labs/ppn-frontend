from django.apps import AppConfig

from api.mixins import ResourceSetupMixin


class AuthConfig(ResourceSetupMixin, AppConfig):
    name = 'api.auth'
    label = 'apiauth'
