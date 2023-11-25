from django.contrib import admin
from .models import JhandiUser


@admin.register(JhandiUser)
class JhandiUserAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'email', 'first_name', 'last_name', 'is_player', 'is_agent', 'is_superuser']