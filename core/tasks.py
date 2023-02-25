from check.celery import app

from .utils import create_check_file


@app.task(name="generate_pdf_file")
def generate_pdf_file(check_id: int, check_type: str, order_detail: dict) -> None:
    """Task for pdf-file generate with check"""
    create_check_file(check_id, check_type, order_detail)
    return None
