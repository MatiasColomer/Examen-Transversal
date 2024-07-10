from django.contrib import admin
from .models import CustomUser, Product, Purchase

admin.site.register(CustomUser)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']
    search_fields = ['name']
    
admin.site.register(Purchase)