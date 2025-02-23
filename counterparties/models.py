from django.db import models

class CounterParties(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    marka_auto = models.CharField(max_length=50)
    number_auto = models.CharField(max_length=50)
    vin_number = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name} {self.surname} {self.last_name}'

    class Meta:
        verbose_name = 'Контрагента в список'
        verbose_name_plural = 'Список контрагентов'