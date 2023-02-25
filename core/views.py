from urllib.parse import quote

import pypdf
from django.http import HttpResponse
from pypdf.errors import PdfReadError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .utils import mark_check_as_printed
from .exceptions import PointWithoutPrintersError, CheckNotRenderedError
from .serializers import OrderSerializer, CheckListSerializer, CheckDetailSerializer
from .models import Printer, Check, CheckStatus


class CreateCheckAPIView(APIView):
    """API for create all checks types in current point for chosen order."""

    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        # If Point doesn't have any printers
        if Printer.objects.filter(point_id=kwargs["point_id"]).count() == 0:
            raise PointWithoutPrintersError()

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        created_checks = serializer.save(order=serializer.validated_data, point_id=kwargs["point_id"])
        return Response(created_checks)


class ListCheckAPIView(ListAPIView):
    """Return collection of checks for chosen printer."""

    serializer_class = CheckListSerializer

    def get_queryset(self):
        """Return queryset of all rendered checks for chosen printer."""
        printer = get_object_or_404(Printer, pk=self.kwargs["printer_id"])
        return Check.objects.filter(printer=printer, status=CheckStatus.RENDERED)


class RetrieveUpdateCheckAPIViewSet(RetrieveModelMixin, GenericViewSet):
    """API for download check file and set check status to PRINTED."""

    queryset = Check.objects.all()
    serializer_class = CheckDetailSerializer

    def get_object(self):
        check = super().get_object()

        if check.status == CheckStatus.NEW:
            raise CheckNotRenderedError()
        return check

    def retrieve(self, request, *args, **kwargs):
        """Endpoint for download check file."""
        check = self.get_object()
        filename = check.pdf_file.name.split('/')[-1]
        output = check.pdf_file

        response = HttpResponse(
            output,
            headers={
                "Content-Type": "application/pdf",
                "Content-Length": len(output),
                "Content-Disposition": f"attachment; filename*=utf-8''{quote(filename)}",
                "Access-Control-Expose-Headers": "*"
            }
        )
        return response

    @action(detail=True, methods=["PATCH"], url_path="update")
    def set_printed(self, request, *args, **kwargs):
        """Endpoint for mark PRINTED for check file."""
        check = self.get_object()
        check.status = CheckStatus.PRINTED
        check.save(update_fields=["status"])

        return Response(status=status.HTTP_204_NO_CONTENT)


class PrintCheckAPIView(APIView):
    """
    API for print check in printer.

    This endpoint emulate print work.
    Its accept check file and print it.
    """

    parser_classes = [FileUploadParser]

    def put(self, request, filename, format=None):
        api_key = request.headers.get("X-API-Key")

        if not api_key:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if "file" not in request.FILES:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        printer = get_object_or_404(Printer, api_key=api_key)
        file_obj = request.data["file"]

        # Check that user upload valid/not corrupted PDF file
        try:
            pypdf.PdfReader(file_obj)
        except PdfReadError:
            raise ValidationError("You must upload a valid PDF file")

        # some printing logic/magic here

        # call functionality for mark that check was successfully printed
        mark_check_as_printed(filename)

        return Response(status=status.HTTP_204_NO_CONTENT)
