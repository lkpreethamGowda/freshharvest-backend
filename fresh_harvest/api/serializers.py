from rest_framework import serializers
from .models import Farmer,Product,Cart,CartItem,Discount,Review, Order , OrderItem , Recipe

from fresh_harvest.users.models import User


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "name", "url"]

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class FarmerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmer
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model= CartItem
        fields='__all__'



class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model= Cart
        fields='__all__'


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True,read_only=True)
    class Meta:
        model=Order
        fields=['user_id','address','amount','estimated_time','status','discount_id','items']


class OrderItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderItem
        fields=['product_id','quantity']

class OrderNewSerializer(serializers.ModelSerializer):
    items=OrderItemCreateSerializer(many=True,write_only=True)
    items_out=OrderItemSerializer(many=True,read_only=True)

    class Meta:
        model=Order

        fields=['id', 'user_id', 'address', 'amount', 'estimated_time','status', 'discount_id', 'items', 'items_out']

    def create(self, validated_data):
        items_data=validated_data.pop('items')
        order=Order.objects.create(**validated_data)

        for item_data in items_data:
            OrderItem.objects.create(order_id=order,**item_data)

        return order    
    

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model= Recipe
        fields= '__all__'











