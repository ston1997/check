import json
import os

import requests
import base64

from django.conf import settings
from django.core.files.base import ContentFile
from django.template.loader import render_to_string
from rest_framework.exceptions import ValidationError

from .models import Check, CheckStatus


def create_check_file(check_id: int, check_type: str, order_detail: dict) -> None:
    check = Check.objects.get(id=check_id)
    order_id = order_detail["id"]
    check_template = render_to_string(
        "core/check_template.html",
        context={
            "order_id": order_id,
            "order_detail": json.dumps(order_detail)
        }
    )

    data = {"contents": base64.b64encode(check_template.encode()).decode()}
    url = settings.WKHTMLTOPDF_API_URL
    response = requests.post(url, json=data)
    check.pdf_file.save(os.path.join("pdf", f"{order_id}_{check_type}.pdf"), ContentFile(response.content))
    check.status = CheckStatus.RENDERED
    check.save(update_fields=["status"])

    return None


def mark_check_as_printed(filename: str) -> None:
    """
    This method set check as PRINTED.

    In current realisation - its fetch check from DB and update it.
    In real case - here could be call to endpoint for update check.
    """
    try:
        check_prefix = filename.split(".pdf")[0]
        order_id, check_type = check_prefix.split("_")
        check = Check.objects.get(order__contains={"id": int(order_id)}, type=check_type)
    except Check.DoesNotExist:
        raise ValidationError(f"Check type: {check_type} for order with ID: {order_id} doesn't exist")
    except:
        raise ValidationError("Invalid file name: it must be '<order_id>_<check_type>.pdf'")

    check.status = CheckStatus.PRINTED
    check.save(update_fields=["status"])
    return None
