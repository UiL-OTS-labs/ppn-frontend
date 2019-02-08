import api.rest as rest


class SuccessResponse(rest.Resource):

    success = rest.BoolField()
