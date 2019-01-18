import inspect

from django.apps import apps

from .options import CollectionOptions, ResourceOptions
from .registry import registry


class ResourceMetaclass(type):
    """Metaclass for all rest. Inspired by Django's ModelBase"""
    _options = ResourceOptions

    def __new__(mcs, name, bases, attrs):
        super_new = super().__new__

        # Also ensure initialization is only performed for subclasses of Model
        # # (excluding Model class itself).
        parents = [b for b in bases if isinstance(b, ResourceMetaclass)]
        if not parents:
            return super_new(mcs, name, bases, attrs)

        module = attrs.pop('__module__')
        new_attrs = {
            '__module__': module
        }
        classcell = attrs.pop('__classcell__', None)
        if classcell is not None:
            new_attrs['__classcell__'] = classcell
        new_class = super_new(mcs, name, bases, new_attrs)
        attr_meta = attrs.pop('Meta', None)

        if not attr_meta:
            meta = getattr(new_class, 'Meta', None)
        else:
            meta = attr_meta

        app_label = None

        # Look for an application configuration to attach the model to.
        app_config = apps.get_containing_app_config(module)

        if getattr(meta, 'app_label', None) is None:
            if app_config is None:
                raise RuntimeError(
                    "resource class %s.%s doesn't declare an explicit "
                    "app_label and isn't in an application in "
                    "INSTALLED_APPS." % (module, name)
                )

            else:
                app_label = app_config.label

        meta = mcs._options(meta, app_label)
        meta.contribute_to_class(new_class, '_meta')

        if 'client' not in attrs:
            new_class.client = meta.client_class()
            new_class.client.contribute_to_class(new_class, 'client')

        # Add all attributes to the class.
        for obj_name, obj in attrs.items():
            new_class.add_to_class(obj_name, obj)

        new_class.register_class()

        return new_class

    def register_class(cls):
        registry.register_resource(cls._meta.app_label, cls)

    def add_to_class(cls, name: str, value: object) -> None:
        """This either runs a class' contribute_to_class method, or adds the
        object to the class as a class attribute.
        """
        # We should call the contribute_to_class method only if it's bound
        if not inspect.isclass(value) and hasattr(value, 'contribute_to_class'):
            value.contribute_to_class(cls, name)
        else:
            setattr(cls, name, value)


class CollectionMetaclass(ResourceMetaclass):
    """Metaclass for all collections. It's basically the ResourceMetaclass
    with different options
    """
    _options = CollectionOptions

    def register_class(cls):
        registry.register_collection(cls._meta.app_label, cls)


class Resource(metaclass=ResourceMetaclass):
    """This class can be extended to describe a REST resource.
    It's inspired by Django's models, and as such, configuring the resource
    is done in a similar manner. Each resource should be defined by creating
    class that extends this one.

    In this class, one can define it's fields by creating class attributes
    containing the appropriate fields (defined in fields.py).

    A resource can be connected to an API endpoint by specifying the path
    at which this resource can be retrieved. This is done by setting the path
    variable in the inline Meta class. This is optional however.

    One might also want to limit the available operations for this resource to
    reflect the API's capabilities. This is done by supplying a list of
    supported operations in the supported_operations variable of the Meta class.

    For a detailed overview of these operations, please see their corresponding
    client methods. (Found in client.py, or by calling help on Resource.client).

    Available Meta variables:
    - path (optional): Specifies the REST endpoint location for this resource.
      Required for client operations. One might leave this unconfigured if the
      resource in question is part of a different resource/collection and does
      not have it's own endpoint.
      Please note that the API host will be joined to the path. Please specify
      a path relative to the host value supplied in settings.py
    - path_variables (optional): A list of variable names that are to be
      included in the path. If a variable name corresponds to a field name, the
      value of said field will be used, otherwise the value will be retrieved
      from the kwargs of the client method call. (Note: if kwargs are used, they
      will not be used in the request body/parameters)
      To specify where in the path these variables should be used, one can add
      '{variable_name}' in the path variable. For example:

      ::code: python

        class Meta:
            path = "/item/{pk}/"
            path_variables = ['pk']

    - identifier_field (optional): TODO: write this after implementation is complete
    - supported_operations (optional): A list of operation the API supports for
      this resource. Does not affect anything if no path is specified.
      Defaults to all operations.
    - client_class (optional): You can use this variable to specify a different
      client.
    - default_return_resource (optional): You can specify a different resource
      class that the API sends back on PUT operations. This is a default value,
      and can be overridden on the operation call itself. See the client
      documentation for more info. If none is supplied, a boolean is returned
      instead.
    """

    _meta = None

    def __init__(self, **kwargs):
        opts = self._meta

        for name, field in opts.fields.items():
            if name in kwargs:
                cleaned_value = field.clean(kwargs[name])
                setattr(self, name, cleaned_value)
            else:
                setattr(self, name, field.default)

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self)

    def __str__(self):
        pk_value = "[unknown]"
        if self._meta.identifier_field:
            pk_value = getattr(self, self._meta.identifier_field, pk_value)
        return '{} object ({})'.format(self.__class__.__name__, pk_value)

    def to_api(self) -> dict:
        """Returns the data in this resource as a dict, to be converted to
        a form the API understands.

        :return: dict
        """
        return {
            name: field.to_api(getattr(self, name)) for (name, field) in
            self._meta.fields.items()
        }

    def put(self, return_resource=None, **kwargs):
        """Proxy method that autofills the obj parameter"""
        self.client.put(self, return_resource=return_resource, **kwargs)

    def delete(self, **kwargs):
        """Proxy method that autofills the obj parameter"""
        self.client.delete(self, **kwargs)


class Collection(metaclass=CollectionMetaclass):
    """This class can be extended to describe a REST collection.
    A collection does not have fields of its own, one needs to specify the
    resource contained in the collection instead. At the moment, a collection
    can only hold one type of resource and cannot hold different collections.

    A collection can be connected to an API endpoint by specifying the path
    at which this resource can be retrieved. This is done by setting the path
    variable in the inline Meta class.This is optional however.

    At the moment, only get operations are supported for collections. You can
    choose plain GET or emulate GET over a POST request for more security.

    Note: you are not able to change the contents of a collection, as this
    would imply you can update the collection in the API. This class have been
    locked down to discourage people from trying to do so.

    For a detailed overview of these operations, please see their corresponding
    client methods. (Found in client.py, or by calling help on Resource.client).

    Available Meta variables:
    - resource (required): The resource class contained in this collection
    - path (optional): Specifies the REST endpoint location for this resource.
      Required for client operations. One might leave this unconfigured if the
      resource in question is part of a different resource/collection and does
      not have it's own endpoint.
      Please note that the API host will be joined to the path. Please specify
      a path relative to the host value supplied in settings.py
    - path_variables (optional): A list of variable names that are to be
      included in the path. If a variable name corresponds to a field name, the
      value of said field will be used, otherwise the value will be retrieved
      from the kwargs of the client method call.
      To specify where in the path these variables should be used, one can add
      '{variable_name}' in the path variable. For example:

      ::code: python

        class Meta:
            path = "/item/{pk}/"
            path_variables = ['pk']

    - operation (optional): Whether to use GET or GET_OVER_POST
      Defaults to GET. Does not affect anything if no path is specified.
    - client_class (optional): You can use this variable to specify a different
      client.
    """
    __slots__ = ['_items']
    _meta = None

    def __init__(self, json):
        opts = self._meta

        try:
            objects = list(json)

            self._items = [opts.resource(**obj) for obj in objects if not
            isinstance(obj, int)]
        except TypeError as e:
            raise e
            pass  # todo: throw error on not-a-list

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __getitem__(self, item):
        return self._items[item]

    def __setitem__(self, key, value):
        raise Exception("'{}' is immutable!".format(self.__class__.__name__))

    def __str__(self):
        return '{} collection for resource {}'.format(
            self.__class__.__name__,
            self._meta.resource.__class__.__name__
        )

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, repr(self._items))

    def to_api(self) -> list:
        """Returns the data in this collection as a list, to be converted to
        a form the API understands.

        :return: dict
        """
        return [item.to_api() for item in self._items]
