import api.rest as rest
from api.resources.generic_resources import SuccessResponse


class Comment(rest.Resource):
    class Meta:
        path = '/api/leader/add_comment/'
        supported_operations = [rest.Operations.put]
        default_return_resource = SuccessResponse

    experiment = rest.IntegerField()

    participant = rest.IntegerField()

    comment = rest.TextField()
