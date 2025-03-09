from django.db import models
from django.contrib.auth.models import User

class CounterParties(models.Model):
    name = models.CharField(max_length=50)
    inn = models.CharField(max_length=12, null=True, blank=True)
    kpp = models.CharField(max_length=50, null=True, blank=True)
    okpo = models.CharField(max_length=50, null=True, blank=True)
    ogrn = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Контрагента в список'
        verbose_name_plural = 'Список контрагентов'

class CounterpartyCars(models.Model):
    counterparty = models.ForeignKey(CounterParties, on_delete=models.CASCADE, related_name='cars')
    full_name = models.CharField(max_length=100)
    number_auto = models.CharField(max_length=50)
    vin_number = models.CharField(max_length=50)
    marka_auto = models.CharField(max_length=50)
    model_auto = models.CharField(max_length=50)
    release_date = models.CharField(max_length=50)

    def __str__(self):
        return self.full_name
    
    class Meta:
        verbose_name = 'Машину в список к контрагенту'
        verbose_name_plural = 'Список машин контрагентов'