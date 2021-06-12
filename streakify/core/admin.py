from django.contrib import admin
from streakify.core.models import Mobile, Country

@admin.register(Mobile)
class MobileAdmin(admin.ModelAdmin):
    model = Mobile
    list_display = ["id", "country_code", "mobile"]
    search_fields = list_display


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    model = Country
    list_display = ["id", "name"]
    search_fields = list_display
