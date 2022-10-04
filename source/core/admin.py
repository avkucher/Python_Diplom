from core.models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Настройка админки пользователя"""
    # Отображаемые поля
    list_display = ('username', 'email', 'first_name', 'last_name')
    search_fields = ('email', 'first_name', 'last_name', 'username')
    # поля только для чтения
    readonly_fields = ('last_login', 'date_joined')
    # поля для фильтров
    list_filter = ('is_staff', 'is_active', 'is_superuser')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (
            'Personal Info',
            {'fields': ('first_name', 'last_name', 'email')}
        ),
        (
            'Permission',
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (
            'Important dates',
            {'fields': ('last_login', 'date_joined')}
        )
    )

# Меняем заголовок админки
admin.site.site_title = 'Администрирование ToDoList'
admin.site.site_header = 'Администрирование ToDoList'