class ApiError(Exception):
    """General API errors"""

    def __init__(self, status_code, message, *args):
        super(ApiError, self).__init__(*args)
        self.status_code = status_code
        self.message = message


class OperationNotEnabled(Exception):
    """Thrown when a call was made to a resource/collection operation that was
    not enabled by it's config."""