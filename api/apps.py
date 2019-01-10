from django.apps import AppConfig

from .mixins import ResourceSetupMixin


class ApiConfig(ResourceSetupMixin, AppConfig):
    name = 'api'
