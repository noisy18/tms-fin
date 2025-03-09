from django.contrib import admin
from counterparties.models import CounterParties, CounterpartyCars

@admin.register(CounterParties)
class CounterPartiesAdmin(admin.ModelAdmin):
    list_display = ('name', 'inn')

@admin.register(CounterpartyCars)
class CounterpartyCarsAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'number_auto', 'vin_number', 'marka_auto', 'model_auto', 'release_date')