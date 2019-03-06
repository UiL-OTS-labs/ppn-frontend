from ..rest import Resource, fields, Operations, ResourceCollection


class ApiGroupResource(Resource):

    pk = fields.IntegerField()

    name = fields.TextField()


class ApiGroupResourceCollection(ResourceCollection):

    class Meta:
        resource = ApiGroupResource


class ApiUserResource(Resource):

    class Meta:
        path = '/api/auth/'
        supported_operations = [Operations.get_over_post]

    id = fields.IntegerField()

    token = fields.TextField()

    is_active = fields.BoolField(default=False)

    is_admin = fields.BoolField(default=False)

    is_ldap_account = fields.BoolField(default=False)

    needs_password_change = fields.BoolField(default=False)

    groups = fields.CollectionField(ApiGroupResourceCollection)
