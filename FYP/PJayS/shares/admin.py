from django.contrib import admin
from .models import Saham

@admin.register(Saham)
class SahamAdmin(admin.ModelAdmin):
    list_display = ('share_id', 'student', 'teacher', 'share_amount', 'share_date', 'share_type')
    search_fields = ('student__nama', 'teacher__nama')
