from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('email', 'fecha', 'estado')
    list_filter = ('estado', 'fecha')
    search_fields = ('email', 'descripcion')
