from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db import models
from django.forms import Textarea

from users.models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    search_fields = ('email', 'username', 'city', 'postal_code')
    list_filter = ('city', 'postal_code', 'date_joined')
    list_display = ('id', 'uuid', 'email', 'username', 'is_active', 'is_staff', 'is_superuser')
    ordering = ("-date_joined",)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal', {'fields': ('first_name', 'last_name', 'address', 'city', 'postal_code','slug')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')})
        
    )
    formfield_overrides = {
        models.TextField : {'widget': Textarea(attrs={'rows': 20, 'cols' : 60})}
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'address', 'city', 'postal_code', 'groups', 'is_staff', 'is_active', 'is_superuser')}
         ),
    )