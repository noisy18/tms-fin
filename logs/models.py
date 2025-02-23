from django.db import models
from django.contrib.auth.models import User

class EntryExitActionLogs(models.Model):
    ACTION_CHOICES = [
        ('add', 'Добавление'),
        ('delete', 'Удаление'),
    ]

    task_id = models.IntegerField()
    task_type = models.CharField(max_length=50)
    number_auto = models.CharField(max_length=50)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timestamp} - {self.user.username} {self.action} задачу {self.task_id} ({self.number_auto}) автора {self.author}"


class TextActionLogs(models.Model):
    ACTION_CHOICES = [
        ('add', 'Добавление'),
        ('delete', 'Удаление'),
    ]

    task_id = models.IntegerField()
    title = models.CharField(max_length=50)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timestamp} - {self.user.username} {self.action} задачу {self.task_id} автора {self.author}"