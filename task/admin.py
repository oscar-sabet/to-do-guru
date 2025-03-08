from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Task


class TaskAdmin(SummernoteModelAdmin):
    summernote_fields = ("description",)


admin.site.register(Task, TaskAdmin)
