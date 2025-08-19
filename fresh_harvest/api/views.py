from django.shortcuts import render

# Create your views here.

from rest_framework.response import Response
from .serializers import ProductSerializer , FarmerSerializer , CartSerializer ,UserSerializers,DiscountSerializer, ReviewSerializer, CartItemSerializer, OrderSerializer,OrderNewSerializer,RecipeSerializer,UserRegistrationSerializer


from .models import Product , Farmer , CartItem ,Cart ,Discount , Review ,Order , OrderItem , Recipe

from rest_framework.viewsets import ModelViewSet
from rest_framework import mixins , viewsets

from rest_framework import status
from rest_framework.decorators import action
from fresh_harvest.users.models import User
from rest_framework import generics, permissions

from django.urls import path
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def currentUser(request):

    user = request.user
    print(user.id)
    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
    })



@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def clear_cart(request, cart_id):
    try:
        cart = Cart.objects.get(id=cart_id)
        cart.items.all().delete()  # delete all CartItem objects related to this cart
        return Response({"detail": "Cart cleared successfully"})
    except Cart.DoesNotExist:
        return Response({"detail": "Cart not found"}, status=404)


class FarmerViewset(ModelViewSet):
    queryset=Farmer.objects.all()
    serializer_class=FarmerSerializer



class UserViewset(ModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializers

class DiscountViewset(mixins.RetrieveModelMixin,mixins.ListModelMixin,viewsets.GenericViewSet):
    queryset=Discount.objects.all()
    serializer_class=DiscountSerializer
    lookup_field='coupon'
  

class ProductViewset(ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
   

class ProductSearchViewset(mixins.RetrieveModelMixin,mixins.ListModelMixin,viewsets.GenericViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    
    

    def get_queryset(self):
        queryset =  super().get_queryset()
        label = self.request.query_params.get('label')
        product_type = self.request.query_params.get('type')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        product_name=self.request.query_params.get('product_name')
        if product_name is not None:
            queryset=queryset.filter(product_name=product_name)

        if label is not None:
            queryset=queryset.filter(label=label)

        if product_type is not None:
            queryset=queryset.filter(type=product_type)

        if min_price is not None:
            queryset=queryset.filter(pricing__gte=min_price)

        if max_price is not None:
            queryset=queryset.filter(pricing__lte=max_price)
        return queryset


class ReviewViewset(ModelViewSet):
    queryset=Review.objects.all()
    serializer_class=ReviewSerializer
    permission_classes=[permissions.AllowAny]

    def get_queryset(self):
        queryset =  super().get_queryset()
        """user_id= self.request.user"""
        product_id =self.request.query_params.get('product_id')
        if product_id is not None:
            queryset=queryset.filter(product_id=product_id)
        return queryset
        
    """def create(self,request,*args,**kwargs):
        user_id=request.user
        data=request.data
        data["User_id"]=user_id
        serializer=self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers=self.get_success_headers(serializer.data)
        return Response(serializer.data,status=status.HTTP_201_CREATED,headers=headers)"""


class CartViewset(mixins.CreateModelMixin,mixins.ListModelMixin,viewsets.GenericViewSet):
    queryset=Cart.objects.all()
    serializer_class=CartSerializer
    

    def get_queryset(self):
        queryset =  super().get_queryset()
        """user_id= self.request.user"""
        user_id=self.request.query_params.get('user_id')
        if user_id is not None:
            queryset=queryset.filter(user_id=user_id)
        return queryset


class CartItemViewset(ModelViewSet):
   
    serializer_class=CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset=CartItem.objects.all()
        cart_id=self.request.query_params.get('cart_id')
        if cart_id is not None:
            queryset=queryset.filter(cart_id=cart_id)
        return queryset
    
    @action(detail=True, methods=['patch'])
    def increment(self, request, pk=None):
        cart_item = self.get_object()
        cart_item.count += 1
        cart_item.save()
        serializer = self.get_serializer(cart_item)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def decrement(self, request, pk=None):
        cart_item = self.get_object()
        if cart_item.count > 1:
            cart_item.count -= 1
            cart_item.save()
        else:
            
            cart_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = self.get_serializer(cart_item)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='add-to-cart')
    def add_to_cart(self, request):
        data = request.data.copy()
        user_id = data.pop('user_id', None)

        if not user_id:
            return Response({"detail": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cart = Cart.objects.get(user_id=user_id)
        except Cart.DoesNotExist:
            return Response({"detail": "Cart for the user does not exist"}, status=status.HTTP_404_NOT_FOUND)

        data['cart_id'] = cart.id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

"""class AddtoCart(mixins.CreateModelMixin,viewsets.GenericViewSet):
    serializer_class = CartItemSerializer
    queryset= CartItem.objects.all()

    def create(self, request, *args, **kwargs):
        #user_Id= request.user
        data=request.data
        user_id=data.pop('user_id')
        
        
        cart=Cart.objects.get(user_id=user_id)
        cart_id=cart.id

        data['cart_id']=cart_id

        serializer= self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,status=status.HTTP_201_CREATED,headers=headers)"""







class DeleteCartItem(mixins.DestroyModelMixin,viewsets.GenericViewSet):
    serializer_class = CartItemSerializer
    queryset= CartItem.objects.all()
    

    def destroy(self,request, *args,**kwargs):
        data= request.data
        user_id=request.data.get('user_id')
        product_id=request.data.get('product_id')

        cart= Cart.objects.get(user_id=user_id)
        cart_id=cart.id
        cart_item =self.get_queryset().get(cart_id=cart_id,product_id=product_id)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
   
    



    

class OrderViewset(mixins.RetrieveModelMixin,mixins.ListModelMixin,viewsets.GenericViewSet):
    queryset=Order.objects.all()
    serializer_class=OrderSerializer
    permission_classes=[permissions.AllowAny]

    def get_queryset(self):
        queryset=Order.objects.all()
        user_id=self.request.query_params.get('user_id')
        if user_id is not None:
            queryset=queryset.filter(user_id=user_id)
        return queryset
        

class OrderAddViewset(ModelViewSet):
    queryset=Order.objects.all()
    serializer_class=OrderNewSerializer
   

class RecipeViewset(ModelViewSet):
    queryset=Recipe.objects.all()
    serializer_class=RecipeSerializer
    permission_classes=[permissions.AllowAny]

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]