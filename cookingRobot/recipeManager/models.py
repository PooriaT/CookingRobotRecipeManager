from enum import unique
from unittest.util import _MAX_LENGTH
from django.db import models

# Here we create tables for our DB.

#UserProfile Class -> referring to user information 
class UserProfile(models.Model):
    pass

#Recipe Class -> Referring to recipe information
class Recipe(models.Model):
    recipeID = models.AutoField(primary_key=True)
    recipeName = models.TextField(max_length=50)
    category = models.TextField(max_length=50, default='')
    ingredient = models.TextField(max_length=400)
    duration = models.DurationField()
    steps = models.TextField(max_length=2000)
    calories = models.FloatField()
    servings = models.FloatField()
    chefName = models.TextField(max_length=50, default='ADMIN')
    
    

#List Class -> Referring to list information
class List(models.Model):
    pass

