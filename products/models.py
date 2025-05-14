from django.db import models

class recipes(models.Model):
    name = models.CharField(max_length=60)
    course = models.CharField(max_length=40)
    descripition = models.TextField()
    Ingredients = models.CharField(max_length=40)

# Create your models here.
