from django.utils.translation import gettext as _

from rest_framework import serializers

from .exceptions import CheckAlreadyPrintedError
from .tasks import generate_pdf_file
from .models import Printer, Check


class OrderSerializer(serializers.Serializer):
    """Serializer for new order"""

    id = serializers.IntegerField(help_text=_("Order ID"))

    def validate(self, attrs):
        # If Checks for this order have already been created
        if Check.objects.filter(order__contains={"id": attrs["id"]}).exists():
            raise CheckAlreadyPrintedError()

        return attrs

    def save(self, **kwargs):
        created_checks = []
        for printer in Printer.objects.filter(point_id=kwargs["point_id"]):
            check = Check.objects.create(
                printer=printer,
                type=printer.check_type,
                order=kwargs["order"]
            )
            created_checks.append(CheckSerializer(instance=check).data)
            print(printer.check_type)
            generate_pdf_file.delay(check.id, printer.check_type, kwargs["order"])

        return created_checks


class CheckListSerializer(serializers.ModelSerializer):
    """Return collection of checks with tiny information."""

    class Meta:
        model = Check
        fields = (
            "id",
            "type",
            "status",
        )


class CheckDetailSerializer(serializers.ModelSerializer):
    """Return detail check information."""
    class Meta:
        model = Check
        fields = "__all__"


class PrinterSerializer(serializers.ModelSerializer):
    """Return printer information."""
    class Meta:
        model = Printer
        fields = (
            "id",
            "name",
            "api_key",
            "check_type",
            "point_id"
        )


class CheckSerializer(serializers.ModelSerializer):
    """Return check information."""
    class Meta:
        model = Check
        fields = (
            "id",
            "printer_id",
            "type",
            "order",
            "status",
            "pdf_file"
        )
