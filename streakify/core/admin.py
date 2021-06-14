from django.contrib import admin
from streakify.core.models import Country


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    model = Country
    list_display = ["id", "name", "country_code"]
    search_fields = list_display
