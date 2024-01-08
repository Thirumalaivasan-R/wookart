from atexit import register
from django.contrib import admin
from .models import *
 
"""
class CategoryAdmin(admin.ModelAdmin):
  list_display = ('name', 'image', 'description')
admin.site.register(Catagory,CategoryAdmin)
"""
 
admin.site.register(Catagory)
admin.site.register(Product)

@admin.register(OrderWithProducts)
class OrderWithProductsAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'user_id', 'address', 'phone_number', 'delivery_mode', 'name', 'quantity', 'item_price', 'total_price']
    readonly_fields = ['order_id', 'user_id', 'address', 'phone_number', 'delivery_mode', 'name', 'quantity', 'item_price', 'total_price']
    list_display_links = None
   
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'address', 'phone_number', 'delivery_mode', 'total_amount', 'created_at']
    readonly_fields = ['id', 'user', 'address', 'phone_number', 'delivery_mode', 'total_amount', 'created_at']

    def has_add_permission(self, request):
        return False  # Disables the ability to add new orders

    def has_change_permission(self, request, obj=None):
        return False  # Disables the change view for individual orders

    def has_delete_permission(self, request, obj=None):
        return False  # Disables the delete view for individual orders