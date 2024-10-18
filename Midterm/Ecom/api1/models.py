from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    image_url = models.CharField(max_length=2083)
    amount = models.IntegerField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class BusketItems(models.Model):
    product = models.CharField(max_length=255)
    amount = models.IntegerField()
    total_price = models.FloatField()
    adress = models.ForeignKey('Adress', on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + '' + str(self.id)

class Adress(models.Model):
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    house = models.IntegerField()
    flat = models.IntegerField()

    def __str__(self):
        return self.city +  ', ' + self.street

class Purchase(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    purch_date = models.DateTimeField(auto_now_add=True)
    adress = models.ForeignKey('Adress', on_delete=models.CASCADE)
    cardLast4nums = models.IntegerField()

    def __str__(self):
        return self.purch_date