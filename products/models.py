from django.db import models

class recipes(models.Model):
    name = models.CharField(max_length=60)
    course = models.CharField(max_length=40)
    descripition = models.TextField()
    Ingredients = models.CharField(max_length=40)
    isfav = models.BooleanField(default=False)

class user(models.Model):
    username = models.CharField(max_length=80)
    password = models.CharField(max_length=100)
    Email = models.EmailField()
    isadmin = models.BooleanField(default=False)
# Create your models here.
