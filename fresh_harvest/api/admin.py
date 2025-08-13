from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import UserProfile, Farmer, Product, Review, Discount, Cart, CartItem, OrderItem, Order, Recipe
# Register your models here.


admin.site.register(UserProfile)
admin.site.register(Farmer)
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Discount)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Recipe)
