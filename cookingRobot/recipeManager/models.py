from email.policy import default
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User



#This make the email field unique for each created user
User._meta.get_field('email')._unique = True


#Ingredient Category Class
class IngredientCategory(models.Model):
    ingredientCategoryID = models.AutoField(primary_key=True)
    ingredientCategoryName = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.ingredientCategoryName

#Ingredient class
class Ingredient(models.Model):
    ingredientID = models.AutoField(primary_key=True)
    ingredientName = models.CharField(max_length=50, unique=True)
    baseCalorie = models.FloatField()
    ingredientCategory = models.ForeignKey('IngredientCategory', on_delete=models.CASCADE)
    ingredientImg = models.ImageField(upload_to ='ingredient', blank=True, null=True, default='default/noImage.jpeg')
    
    def __str__(self):
        return self.ingredientName

#Utensils Class
class Utensil(models.Model):
    utensilID = models.AutoField(primary_key=True)
    utensilName = models.CharField(max_length=50, unique=True)
    utensilImg = models.ImageField(upload_to ='utensil', blank=True, null=True, default='default/noImage.jpeg') 
    
    def __str__(self):
        return self.utensilName
    
#Category class
class RecipeCategory(models.Model):
    categoryID = models.AutoField(primary_key=True)
    categoryName = models.CharField(max_length=50, unique=True) 
    
    def __str__(self):
        return self.categoryName

#Recipe Class -> Referring to recipe information
class Recipe(models.Model):
    recipeID = models.AutoField(primary_key=True)
    recipeName = models.CharField(max_length=50) 
    category = models.ManyToManyField(RecipeCategory, related_name="recipeCategory")
    ingredient = models.ManyToManyField(Ingredient, related_name="ingredients")
    ingredientAmount = models.JSONField(default=dict, blank=True, null=True)
    utensil = models.ManyToManyField(Utensil, related_name="utensils", blank=True)
    duration = models.DurationField()
    steps = models.TextField(max_length=3000)
    servings = models.FloatField()
    calories = models.FloatField()
    rating = models.FloatField(default=0)
    numRater = models.IntegerField(default=0)
    raters = models.JSONField(default=dict, blank=True, null=True)
    recipeImg = models.ImageField(upload_to ='recipe', blank=True, null=True, default='default/noImage.jpeg')
    chefID = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    chefName = models.CharField(max_length=50, default='admin')
    
    def __str__(self):
        return self.recipeName
    

#List Class -> Referring to list information
class List(models.Model):
    pass

