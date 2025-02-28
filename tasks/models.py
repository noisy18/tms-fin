from django.db import models
from django.contrib.auth.models import User

class TextTasks(models.Model):
    title = models.CharField('Заголовок задачи', max_length=50)
    full_text = models.TextField('Текст задачи', blank=True, null=True)
    date = models.DateField('Дата публикации задачи', null=True)
    time = models.TimeField('Время публикации задачи', null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    is_completed = models.BooleanField('Статус - Завешена', default=False)
    completed_at = models.DateTimeField('Время завершения', null=True, blank=True)
    completed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="completed_tasks")

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Текстовую задачу'
        verbose_name_plural = 'Текстовые задачи'

class EntryTasks(models.Model):
    number_auto = models.CharField('Гос. Номер авто', max_length=50, blank=False, null=True)
    marka_auto = models.CharField('Марка авто', max_length=50, blank=False, null=True)
    name_organization = models.CharField('Наименование организции', max_length=50, blank=False, null=True)
    date = models.DateField('Дата въезда', null=True)
    time = models.TimeField('Время въезда', null=True)
    description = models.TextField('Дополнительная информация', blank=True, null=True)
    is_allowed = models.BooleanField('Вьезд разрешён или запрещён', default=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    date_time_add = models.DateTimeField('Дата, время добавления задачи', blank=True, null=True, auto_now_add=True)

    is_completed = models.BooleanField('Статус - Завешена', default=False)
    completed_at = models.DateTimeField('Время завершения', null=True, blank=True)
    completed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="completed_entry_tasks")


    def __str__(self):
        return str(self.number_auto) if self.number_auto else 'Номер авто не введен'
    
    class Meta:
        verbose_name = 'Машину на въезд'
        verbose_name_plural = 'Машины на въезд'

class ExitTasks(models.Model):
    number_auto = models.CharField('Гос. Номер авто', max_length=50, blank=False, null=True)
    marka_auto = models.CharField('Марка авто', max_length=50, blank=False, null=True)
    name_organization = models.CharField('Наименование организции', max_length=50, blank=False, null=True)
    date = models.DateField('Дата выезда', null=True)
    time = models.TimeField('Время выезда', null=True)
    description = models.TextField('Дополнительная информация', blank=True, null=True)
    is_allowed = models.BooleanField('Выезд разрешён или запрещён', default=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    date_time_add = models.DateTimeField('Дата, время добавления задачи', blank=True, null=True, auto_now_add=True)

    is_completed = models.BooleanField('Статус - Завешена', default=False)
    completed_at = models.DateTimeField('Время завершения', null=True, blank=True)
    completed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="completed_exit_tasks")

    def __str__(self):
        return str(self.number_auto) if self.number_auto else 'Номер авто не введен'
    
    class Meta:
        verbose_name = 'Машину на выезд'
        verbose_name_plural = 'Машины на выезд'


class KontragentTasks(models.Model):
    number_auto = models.CharField('Гос. Номера авто', max_length=50, blank=False, null=True)
    description = models.TextField('Дополнительная информация', blank=True, null=True)
    date_entry = models.DateTimeField('Время ВЪЕЗДА контрагента', blank=True, null=True, auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="add_kontragent")

    is_completed = models.BooleanField('Статус - Завешена', default=False)
    date_exit = models.DateTimeField('Время ВЫЕЗДА контрагента', blank=True, null=True)
    completed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="leave_kontragent")

    def __str__(self):
        return str(self.number_auto) if self.number_auto else 'Номер авто не введен'

    class Meta:
        verbose_name = 'Контрагента'
        verbose_name_plural = 'Контрагенты'

class DeliveryTasks(models.Model):
    number_auto = models.CharField('Гос. Номера авто', max_length=50, blank=False, null=True)
    description = models.TextField('Дополнительная информация', blank=True, null=True)
    date_entry = models.DateTimeField('Время ВЪЕЗДА доставки', blank=True, null=True, auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="add_delivery")

    is_completed = models.BooleanField('Статус - Завешена', default=False)
    date_exit = models.DateTimeField('Время ВЫЕЗДА доставки', blank=True, null=True)
    completed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="leave_delivery")

    def __str__(self):
        return str(self.number_auto) if self.number_auto else 'Номер авто не введен'

    class Meta:
        verbose_name = 'Доставку'
        verbose_name_plural = 'Доставки'