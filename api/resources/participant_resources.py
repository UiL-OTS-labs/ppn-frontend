import api.rest as rest

from .generic_resources import SuccessResponse


class MailinglistSubscribe(rest.Resource):
    class Meta:
        path = '/api/participant/subscribe_mailinglist/'
        supported_operations = [rest.Operations.put]
        default_return_resource = SuccessResponse

    email = rest.TextField()

    language = rest.TextField()

    multilingual = rest.TextField()

    dyslexic = rest.BoolField()
