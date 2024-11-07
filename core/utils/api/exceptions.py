from rest_framework.exceptions import APIException


class CustomValidationException(APIException):
    status_code = 400
    default_detail = 'Error in validating data'

    def __init__(self, detail=None):
        if detail is not None:
            self.detail = detail
        else:
            self.detail = self.default_detail