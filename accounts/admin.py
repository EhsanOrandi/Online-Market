from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import AdminPasswordChangeForm
from .models import User, Email, Address, Shop
from django.utils.translation import gettext_lazy as _

# Register your models here.

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'mobile', 'is_staff']
    password_change_form = AdminPasswordChangeForm
    ordering = ['email', ]
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2')
        }),
    )
    fieldsets = (
        (_('authentication data'), {
            "fields": (
                'email',
                'password',
            ),
        }),
        (_('Personal info'), {
            "fields": ('first_name', 'last_name', 'avatar')
        }),
        (_('Permissions'), {
            "fields": ('is_staff', 'is_active', 'is_superuser',)
        })
    )


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('subject', 'body')
    search_fields = ('subject',)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'zip_code')
    search_fields = ('user', 'zip_code')
    list_filter = ('city',)


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'slug')
    search_fields = ('name', 'slug')
