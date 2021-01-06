from django.contrib import admin
from .models import Order
# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'updated_at')
    date_hierarchy = 'updated_at'