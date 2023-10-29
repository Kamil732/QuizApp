from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

class UserAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff',) 
    search_fields = ('email', 'username',)
    ordering = ('email', 'username',)
    readonly_fields = ('date_joined', 'last_login',)

    filter_horizontal = ()
    list_filter = ()

    add_fieldsets = (
        ('Login info', {'fields': ('username', 'password1', 'password2',)}),
        ('Personal info', {'fields': ('email', 'image_url', 'facebook', 'website',)}),
    )

    fieldsets = (
        ('Login info', {'fields': ('username', 'password',)}),
        ('Personal info', {'fields': ('email', 'image_url', 'facebook', 'website',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_admin',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined', 'slug',)}),
    )

admin.site.register(User, UserAdmin)