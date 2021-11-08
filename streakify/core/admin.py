# Core Django Imports
from django.contrib import admin

# Third-party app imports
from import_export.admin import ImportExportModelAdmin

# Local imports
from .models import ImageModel


@admin.register(ImageModel)
class ImageAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["id"]
