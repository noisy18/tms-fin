from django.db import models
from django.contrib.auth.models import User

class NewCar(models.Model):
    vin_number = models.CharField(max_length=50)
    description = models.CharField(max_length=50, blank=True, null=True)
    date_entry = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    is_completed = models.BooleanField(default=False)
    date_exit = models.DateTimeField(blank=True, null=True)
    completed_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)


    def __str__(self):
        return self.vin_number
    
    class Meta:
        verbose_name = 'Новую машину'
        verbose_name_plural = 'Новые машины'