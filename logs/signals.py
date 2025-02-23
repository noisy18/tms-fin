from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .context_processors import get_current_user

from tasks.models import (
    TextTasks,
    EntryTasks,
    ExitTasks
)
from .models import (
    TextActionLogs,
    EntryExitActionLogs
)

TASK_MODEL = [EntryTasks, ExitTasks]

# Сигналы для машины на въезд и выезд
def entry_exit_log_action(instance, action, task_type):
    current_user = get_current_user()
    EntryExitActionLogs.objects.create(
        task_id = instance.id,
        task_type = task_type,
        number_auto = instance.number_auto,
        action = action,
        author = instance.author.username,
        user = current_user,
    )

for model in TASK_MODEL:
    @receiver(post_save, sender=model)
    def log_task_save(sender, instance, created, **kwargs):
        action = 'add'
        entry_exit_log_action(instance, action, sender.__name__)

    @receiver(post_delete, sender=model)
    def log_task_delete(sender, instance, **kwargs):
        action = 'delete'
        entry_exit_log_action(instance, action, sender.__name__)

# Сигналы для текстовой задачи
@receiver(post_save, sender=TextTasks)
def text_log_save(sender, instance, **kwargs):
    current_user = get_current_user()
    TextActionLogs.objects.create(
        task_id = instance.id,
        title = instance.title,
        action = 'add',
        author = instance.author.username,
        user = current_user,
    )

@receiver(post_delete, sender=TextTasks)
def text_log_delete(sender, instance, **kwargs):
    current_user = get_current_user()
    TextActionLogs.objects.create(
        task_id = instance.id,
        title = instance.title,
        action = 'delete',
        author = instance.author.username,
        user = current_user,
    )