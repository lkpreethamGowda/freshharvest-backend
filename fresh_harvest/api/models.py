from django.db import models

# Create your models here.
from django.conf import settings 

from django.contrib.auth.models import User
from .constants import label_choices , type_choices , status_choices
from django.conf import settings

# Create your models here.

class UserProfile(models.Model):
    user =models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    location = models.CharField(max_length=255, blank=True)


class Farmer(models.Model):
    name=models.CharField(max_length=150)
    location=models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    comment=models.TextField()


class Product(models.Model):
    product_name=models.CharField(max_length=50)
    
    farmer_id=models.ForeignKey(Farmer,blank=False,null=True,on_delete=models.CASCADE)
    image=models.CharField(max_length=255)
    harversted_date=models.DateField()
    location=models.CharField(max_length=255)
    label=models.CharField(choices=(label_choices))
    pricing=models.IntegerField()
    delevery=models.CharField(max_length=150)
    type=models.CharField(choices=(type_choices))

class Review(models.Model):
    user_id=models.ForeignKey(settings.AUTH_USER_MODEL,blank=False,null=True,on_delete=models.SET_NULL)
    product_id=models.ForeignKey(Product,blank=False,null=True,on_delete=models.CASCADE)
    stars=models.IntegerField()
    comments=models.TextField()
    likes=models.IntegerField(default=0)
    dislikes=models.IntegerField(default=0)
    date=models.DateField(auto_now=True)


class Discount(models.Model):
    coupon=models.CharField(max_length=50, unique=True)
    percentage=models.IntegerField()


class Cart(models.Model):
    user_id=models.ForeignKey(settings.AUTH_USER_MODEL,null=False,blank=False,on_delete=models.CASCADE)


class CartItem(models.Model):
    cart_id=models.ForeignKey(Cart, on_delete=models.CASCADE,related_name='items')
    product_id=models.ForeignKey(Product, on_delete=models.CASCADE)
    count=models.IntegerField()


class Order(models.Model):
    
    user_id=models.ForeignKey(settings.AUTH_USER_MODEL,null=False,blank=False,on_delete=models.CASCADE)
    address=models.CharField(max_length=255)
    amount=models.IntegerField()
    estimated_time=models.DateField()
    status=models.CharField(choices=status_choices)
    discount_id=models.ForeignKey(Discount,null=True,blank=True,on_delete=models.SET_NULL)

class OrderItem(models.Model):
    order_id=models.ForeignKey(Order, on_delete=models.CASCADE,related_name='items')
    product_id=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.IntegerField(null=False)

class Recipe(models.Model):
    ingredients = models.TextField()
    steps=models.TextField()
    tips=models.TextField()