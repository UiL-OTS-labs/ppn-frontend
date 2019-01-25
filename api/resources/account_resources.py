import api.rest as rest


class ChangePasswordResponse(rest.Resource):

    success = rest.BoolField()


class ChangePassword(rest.Resource):
    class Meta:
        path = '/api/account/change_password/'
        supported_operations = [rest.Operations.put]
        default_return_resource = ChangePasswordResponse

    current_password = rest.TextField()

    new_password = rest.TextField()
