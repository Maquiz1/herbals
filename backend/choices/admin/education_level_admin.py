# choices/admin/education_level_admin.py

from django.contrib import admin
from choices.models.education_level_model import EducationLevel


@admin.register(EducationLevel)
class EducationLevelAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'name']
    ordering = ['id']
    search_fields = ['code', 'name']