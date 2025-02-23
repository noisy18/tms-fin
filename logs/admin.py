from django.contrib import admin
from .models import TextActionLogs, EntryExitActionLogs

admin.site.register(TextActionLogs)
admin.site.register(EntryExitActionLogs)