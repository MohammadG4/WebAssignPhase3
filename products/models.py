from django.db import models
from django.contrib.auth.models import User

class recipes(models.Model):
    name = models.CharField(max_length=60)
    course = models.CharField(max_length=40)
    descripition = models.TextField()
    Ingredients = models.CharField(max_length=100)
    isfav = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(recipes, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s favorite: {self.recipe.name}"