from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    role = models.SmallIntegerField(choices=(
        (1, 'director'),
        (2, 'waiter'),
        (3, 'manager'),
        (4, 'cooker'),
        (5, 'call-center'),
    ), null=True, blank=True)
    number = models.BigIntegerField(null=True, blank=True)


class BotInfo(models.Model):
    text = models.CharField(max_length=255)


class BotDetail(models.Model):
    text = models.TextField()
    phone = models.CharField(max_length=255)
    lat = models.CharField(max_length=255)
    lng = models.CharField(max_length=255)


class Rooms(models.Model):
    number = models.CharField(max_length=255, unique=True)
    places = models.IntegerField()
    busy = models.BooleanField(default=False)


class Client(models.Model):
    name = models.CharField(max_length=1212)
    phone = models.IntegerField(unique=True)


class Category(models.Model):
    name = models.CharField(max_length=210)

    def __str__(self):
        return self.name


class Food(models.Model):
    name = models.CharField(max_length=23232)
    price = models.IntegerField()
    available = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)


class Product(models.Model):
    name = models.CharField(max_length=210)
    price = models.IntegerField()
    quantity = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    available = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        quantity = int(self.quantity)
        if quantity <= 0:
            self.available = False
        else:
            self.available = True
        super(Product, self).save(*args, **kwargs)


class Order(models.Model):
    user = models.ForeignKey(User,  on_delete=models.CASCADE, null=True, blank=True)
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE, null=True, blank=True)
    delivery = models.BooleanField(default=False)
    owner = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=210, null=True, blank=True)
    date = models.DateField(null=True,blank=True)
    delivery_date = models.DateField(null=True, blank=True)
    done = models.BooleanField(default=False)
    bill = models.IntegerField(null=True, blank=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField()
    done = models.BooleanField(default=False)


class OrderDay(models.Model):
    day = models.DateField(null=True, blank=True)


class Bot(models.Model):
    text = models.TextField()
    name = models.CharField(max_length=2323)


