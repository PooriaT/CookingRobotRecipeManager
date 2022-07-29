from enum import unique
from unittest.util import _MAX_LENGTH
from django.db import models

# Here we create tables for our DB.


#Ingredients Category
class IngCategory(models.Model):
    categoryID = models.AutoField(primary_key=True)
    categoryName = models.CharField(max_length=50)

#Ingredients
class Ingredients(models.Model):
    ingID = models.AutoField(primary_key=True)
    ingName = models.CharField(max_length=50)
    ingCalPerHundered = models.FloatField()
    ingCategory = models.ForeignKey('IngCategory', on_delete=models.CASCADE, blank=True) #one to many

#Recipe Category
class RecipeCategory(models.Model):
    categoryID = models.AutoField(primary_key=True)
    categoryName = models.CharField(max_length=50)

#Utensils
class Utensils(models.Model):
    utensilID = models.AutoField(primary_key=True)
    utensilName = models.CharField(max_length=50)

#Recipe Class -> Referring to recipe information
class Recipe(models.Model):
    recipeID = models.AutoField(primary_key=True)
    recipeName = models.CharField(max_length=50)
    category = models.ManyToManyField(RecipeCategory) #many to many
    ingredient = models.ManyToManyField(Ingredients) #many to many
    duration = models.DurationField()
    steps = models.CharField(max_length=2000)
    servings = models.FloatField()
    chefName = models.TextField(max_length=50, default='ADMIN')
    recipeUtensil = models.ForeignKey('Utensils', on_delete=models.CASCADE, blank=True)
    
    

#List Class -> Referring to list information
class List(models.Model):
    pass

