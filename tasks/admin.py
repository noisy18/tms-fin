from django.contrib import admin
from .models import TextTasks, EntryTasks, ExitTasks, KontragentTasks, DeliveryTasks

admin.site.register(TextTasks)
admin.site.register(EntryTasks)
admin.site.register(ExitTasks)
admin.site.register(KontragentTasks)
admin.site.register(DeliveryTasks)