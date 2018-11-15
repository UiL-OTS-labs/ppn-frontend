"""This module contains an abstraction layer for REST API calls.

It defines the ::class:Resource and ::class:Collection classes, as well as
several resource fields in ::mod:fields.

A collection is a list of resources. Collections can only be retrieved at the
moment.

A resource is a single entity, which contains fields. A resource can be
retrieved on it's own, or through a collection.

Through the means of fields, both Resources and Collections can be parts of
Resources. A collection can only hold a certain resource.

In a less abstract way: a resource is a JSON object, a collection is a JSON list
and fields are JSON fields.

For implementation details, see the :class:Resource and :class:Collection
classes.
"""

from .base import Resource, Collection
from .fields import *
from .options import Operations
