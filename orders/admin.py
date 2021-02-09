from django.contrib import admin
from .models import Order, OrderItem
# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'updated_at')
    date_hierarchy = 'updated_at'
    inlines = [OrderItemInline, ]
