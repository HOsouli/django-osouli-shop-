from django.contrib import admin
from .models import Order,OrderDetails, OrderState

class OrderDetailsInlineAdmin(admin.TabularInline):
    model=OrderDetails
    extra=3

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=['customer','order_state','register_date','is_finally','discount']
    inlines=[OrderDetailsInlineAdmin,]

@admin.register(OrderState)
class OrderStateAdmin(admin.ModelAdmin):
    list_display=('id', 'order_state_title')
