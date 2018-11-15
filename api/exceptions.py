class ApiError(Exception):
    """General API errors"""


class OperationNotEnabled(Exception):
    """Thrown when a call was made to a resource/collection operation that was
    not enabled by it's config."""