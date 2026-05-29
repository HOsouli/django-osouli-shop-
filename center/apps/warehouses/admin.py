from django.contrib import admin
from .models import Warehouse, WarehouseType

@admin.register(WarehouseType)
class WarehouseTypeAdmin(admin.ModelAdmin):
    list_display=['id','warehouse_type_title']

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display=['product','price','quantity','warehouse_type','register_date']
    search_fields = ['product__product_name',]
