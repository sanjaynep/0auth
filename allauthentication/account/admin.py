from django.contrib import admin
from .models import User
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'is_active', 'is_staff', 'is_superuser', 'created_at', 'updated_at')
    search_fields = ('email', 'full_name')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    ordering = ('-created_at',)

# Register your models here.
