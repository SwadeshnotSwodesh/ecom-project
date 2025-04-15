from django.contrib import admin
from .models import *

# admin.site.register(Customer)
# admin.site.register(Product)
# admin.site.register(Order)
# admin.site.register(OrderItem)
# admin.site.register(ShippingAddress)
# admin.site.register(Category)

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'digital', 'category', 'image')  # Display image field

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
