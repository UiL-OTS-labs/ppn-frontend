import api.rest as rest


class SuccessResponse(rest.Resource):
    """
    Generic response resource.

    It's used for most resource that command the backend to do something.
    """

    success = rest.BoolField()
