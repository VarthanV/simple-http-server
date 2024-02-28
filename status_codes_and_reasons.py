
from enum import Enum

# Comprehensive list can be found here
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
# Adding only codes that we will be using
class StatusCode(Enum):
    OK = 200
    NOT_FOUND = 404
    BAD_REQUEST = 400
    INTERNAL_SERVER_ERROR=500

class StatusReason(Enum):
    OK = 'OK'
    NOT_FOUND = 'Not Found'
    BAD_REQUEST = 'Bad Request'
    INTERNAL_SERVER_ERROR = 'Internal Server Error'