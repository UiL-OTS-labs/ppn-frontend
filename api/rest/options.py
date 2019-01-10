from enum import Enum
from django.core.exceptions import ImproperlyConfigured


class Operations(Enum):
    get = 1
    put = 2
    delete = 3
    get_over_post = 4  # When request params should be sent over POST instead of GET. Mostly for logging in


class ResourceOptions:

    def __init__(self, meta, app_label):
        self.meta = meta
        self.resource = None
        self.path = None
        self.path_variables = []
        self.fields = {}
        self.identifier_field = 'id'
        self.supported_operations = [Operations.delete, Operations.get, Operations.put]
        self.client_class = None
        self.default_return_resource = None
        self.app_label = app_label

    def contribute_to_class(self, cls, name):
        setattr(cls, name, self)
        self.resource = cls

        if self.meta:
            meta_attrs = self.meta.__dict__.copy()
            for key, value in meta_attrs.items():
                if key in self.__dict__:
                    self.__dict__[key] = value

        if not self.client_class:
            from .client import ResourceClient
            self.client_class = ResourceClient

    def add_field(self, field):
        self.fields[field.name] = field

    def __str__(self):
        return "{} for {}".format(self.__class__.__name__, self.resource)


class CollectionOptions:

    def __init__(self, meta, app_label):
        self.meta = meta
        self.collection = None
        self.resource = None
        self.path = None
        self.path_variables = []
        self.operation = Operations.get
        self.client_class = None
        self.app_label = app_label

    def contribute_to_class(self, cls, name):
        setattr(cls, name, self)
        self.collection = cls

        if self.meta:
            meta_attrs = self.meta.__dict__.copy()
            for key, value in meta_attrs.items():
                if key in self.__dict__:
                    self.__dict__[key] = value

            if not self.resource:
                raise ImproperlyConfigured("Collections need to have a resource configured in its Meta class")

        if not self.client_class:
            from .client import CollectionClient
            self.client_class = CollectionClient

    def __str__(self):
        return "{} for {}".format(self.__class__.__name__, self.collection)