from django.apps import AppConfig

from uil.rest_client.mixins import ResourceSetupMixin


class AuthConfig(ResourceSetupMixin, AppConfig):
    name = 'api.auth'
    label = 'apiauth'
