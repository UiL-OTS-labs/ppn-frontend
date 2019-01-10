from django.apps import AppConfig

from api.mixins import ResourceSetupMixin


class MainConfig(ResourceSetupMixin, AppConfig):
    name = 'main'
