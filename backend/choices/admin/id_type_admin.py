# choices/admin/id_type_admin.py

from django.contrib import admin
from choices.models.id_type_model import IDType


@admin.register(IDType)
class IDTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'name']
    ordering = ['id']
    search_fields = ['code', 'name']