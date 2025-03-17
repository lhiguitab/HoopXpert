from django.db import models

# Create your models here.
class player(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    height = models.FloatField()
    weight = models.FloatField()
    position = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
