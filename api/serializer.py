from rest_framework import serializers
from main.models import *


class Food_serializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'


class Product_serializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class Rooms_serializer(serializers.ModelSerializer):
    class Meta:
        model = Rooms
        fields = '__all__'


class Category_serializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class Order_serializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'



class Order_item_serializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'



class BotInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotInfo
        fields = '__all__'


class BotDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotDetail
        fields = '__all__'
