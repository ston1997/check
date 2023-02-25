from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _


class CheckType(models.TextChoices):
    KITCHEN = "KITCHEN"
    CLIENT = "CLIENT"


class CheckStatus(models.TextChoices):
    NEW = "NEW"
    RENDERED = "RENDERED"
    PRINTED = "PRINTED"


class Printer(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("Назва принтеру"))
    api_key = models.CharField(max_length=200, unique=True)
    check_type = models.CharField(max_length=200, choices=CheckType.choices, verbose_name=_("Тип чеку"))
    point_id = models.IntegerField(editable=True, verbose_name=_("ID точки"))

    class Meta:
        verbose_name = _("Принтер")
        verbose_name_plural = _("Принтери")

    def __str__(self):
        return self.name


class Check(models.Model):
    printer = models.ForeignKey(Printer, related_name="checks", on_delete=models.CASCADE)
    type = models.CharField(max_length=200, choices=CheckType.choices, verbose_name=_("Тип чеку"))
    order = models.JSONField(default=dict, verbose_name=_("Інформація про замовлення"))
    status = models.CharField(max_length=200, choices=CheckStatus.choices, default=CheckStatus.NEW, verbose_name=_("Статус чеку"))
    pdf_file = models.FileField(null=True, blank=True)

    class Meta:
        verbose_name = _("Чек")
        verbose_name_plural = _("Чеки")

    def __str__(self):
        return self.status

    def get_absolute_url(self):
        return reverse('core:check_detail', args=[self.printer, self.id])
