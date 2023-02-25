from django.contrib import admin

from .models import Printer, Check


class CheckInline(admin.StackedInline):
    model = Check


@admin.register(Printer)
class PrinterAdmin(admin.ModelAdmin):
    list_display = ['name', 'check_type', 'point_id']
    list_filter = ['name', 'check_type']
    inlines = [CheckInline]
    prepopulated_fields = {'api_key': ('api_key',)}


@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    list_display = ['id', 'printer_id', 'order', 'type', 'status', 'pdf_file']
    list_filter = ['printer_id', 'type', 'status']
