from django.apps import AppConfig

from uil.rest_client.mixins import ResourceSetupMixin


class ApiConfig(ResourceSetupMixin, AppConfig):
    name = 'api'
