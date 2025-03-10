from django.contrib import admin

from newcars.models import NewCar

# Register your models here.

@admin.register(NewCar)
class NewCarAdmin(admin.ModelAdmin):
    list_display = ('vin_number', 'description')