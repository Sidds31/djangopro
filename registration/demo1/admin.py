from django.contrib import admin
from . models import Product, Cart
# Register your models here.
@admin.register(Product)
class ProductModeAdmin(admin.ModelAdmin):
    list_display = ('id','title','discounted_price','category','product_image')

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']