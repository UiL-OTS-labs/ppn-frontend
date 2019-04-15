import api.rest as rest

from .generic_resources import SuccessResponse


class UserCreationResponse(SuccessResponse):
    message = rest.TextField()


class ChangePassword(rest.Resource):
    class Meta:
        path = '/api/account/change_password/'
        supported_operations = [rest.Operations.put]
        default_return_resource = SuccessResponse

    current_password = rest.TextField()

    new_password = rest.TextField()


class ForgotPasswordResponse(rest.Resource):

    success = rest.BoolField()

    ldap_blocked = rest.BoolField()


class ForgotPassword(rest.Resource):
    class Meta:
        path = '/api/account/forgot_password/'
        supported_operations = [rest.Operations.put]
        default_return_resource = ForgotPasswordResponse

    email = rest.TextField()


class ValidateToken(rest.Resource):
    class Meta:
        path = '/api/account/validate_token/'
        supported_operations = [rest.Operations.put]
        default_return_resource = SuccessResponse

    token = rest.TextField()


class ResetPassword(rest.Resource):
    class Meta:
        path = '/api/account/reset_password/'
        supported_operations = [rest.Operations.put]
        default_return_resource = SuccessResponse

    token = rest.TextField()

    new_password = rest.TextField()
