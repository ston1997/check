from django.utils.translation import gettext as _

from rest_framework import status
from rest_framework.exceptions import APIException


class CheckAlreadyPrintedError(APIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = _("Checks for this order have already been created")


class PointWithoutPrintersError(APIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = _("Point doesn't have any printers")


class CheckNotRenderedError(APIException):
    status_code = status.HTTP_424_FAILED_DEPENDENCY
    default_detail = _("Check has incompatible status")
