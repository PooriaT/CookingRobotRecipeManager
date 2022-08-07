import re
from django.shortcuts import render, redirect
from django.template import loader

from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

import json
#from django.core import serializers
from datetime import datetime, timedelta

from .models import IngredientCategory
from .models import Ingredient
from .models import Utensil
from .models import Recipe
from .models import RecipeCategory
from .models import List

########################################
#Homepage 
def index(request):
    message = "No Result!"
    allRecipe = Recipe.objects.all()
    
    
    user_fname = ', Guest'
    login_stat = True
    if request.user.is_authenticated:
        user_fname = ', ' + request.user.get_short_name()
        login_stat = False
    
    submittedValue = request.POST
    if bool(submittedValue):
        if 'sortSubmit' in submittedValue:
            if submittedValue["sortSubmit"] != 'default':
                item = submittedValue["sortSubmit"]
                allRecipe = allRecipe.order_by(item)
        elif 'search' in submittedValue:
            item = submittedValue['search']
            searchFor = submittedValue['searchFor']
            if item == "recipeName":
                allRecipe = allRecipe.filter(recipeName__contains=searchFor)
            elif item == "chefName":
                allRecipe = allRecipe.filter(chefName__contains=searchFor)
            else:
                allRecipe = {}

        
    template = loader.get_template('recipeManager/index.html')
    
    context = {
        'loginStat' : login_stat,
        'name' : user_fname,
        'allRecipe': allRecipe,
        'message' : message,
    }
    
    return HttpResponse(template.render(context, request))

########################################
#The function related to adding new Ingredient 
def newRecipe(request):
    message = ""
    
    allRecipeCategory = RecipeCategory.objects.all()
    allIngredientCategory = IngredientCategory.objects.all()
    allIngredient = Ingredient.objects.all()
    allUtensil = Utensil.objects.all()
    
    #allUtensil = serializers.serialize("json", Utensil.objects.all()) # list(allUtensil.values())
    
    user_fname = ', Guest'
    login_stat = True
    if request.user.is_authenticated:
        user_fname = ', ' + request.user.get_short_name()
        login_stat = False
        template = loader.get_template('recipeManager/newRecipe.html')
        
        print(request.POST)
        if request.POST:
            name = request.POST['recipeName']
            category = request.POST.getlist('category')
            ingredient = request.POST.getlist('ingredient')
            amount = request.POST.getlist('amount')
            
            ingredientAmount = {}
            for i in range(len(ingredient)):
                ingredientAmount[ingredient[i].strip()] = amount[i]
            
            ingredientAmount = json.dumps(ingredientAmount)
            utensil = request.POST.get('utensil')
            duration = request.POST['duration']#str(int(request.POST['duration']) * 3600)
            steps = request.POST['steps']
            servings = request.POST['servings']
            calories = request.POST['calories']
            
            
                
            chefName = request.user.get_full_name()
            
            duration = timedelta(hours= float(duration))
            print(duration)
            newItem = Recipe.objects.create(recipeName = name,
                                            ingredientAmount = ingredientAmount,
                                            duration = duration,
                                            steps = steps,
                                            servings = servings,
                                            calories = calories,
                                            chefName = chefName,
                                            )
            print(ingredientAmount)
            if request.POST['ingredientImg']:
                imgDir = request.POST['ingredientImg']
                newItem.recipeImg.add(imgDir)
                
            if category:
                for item in category:
                    newItem.category.add(RecipeCategory.objects.get(categoryName = item))       
            if ingredient:
                for item in ingredient:
                    newItem.ingredient.add(Ingredient.objects.get(ingredientName = item.strip())) 
            if utensil:    
                for item in utensil:
                    newItem.utensil.add(Utensil.objects.get(utensilName = item.strip())) 
                          
            # newItem.save()
            return redirect('index') 
        
        context = {
            'loginStat' : login_stat,
            'name' : user_fname,
            'allRecipeCategory' : allRecipeCategory,
            'allIngredientCategory' : allIngredientCategory,
            'allIngredient' : allIngredient,
            'allUtensil' : allUtensil,
            'message' : message,
        }
        
        return HttpResponse(template.render(context, request))
    
    else:
        return redirect('index') 
    

########################################
#Query for Ingredients
def ingredient(request):
    message = "There is no available ingredient!!!"
    allIngredientCategory = IngredientCategory.objects.all()
    allIngredient = Ingredient.objects.all()
    
    user_fname = ', Guest'
    login_stat = True
    if request.user.is_authenticated:
        user_fname = ', ' + request.user.get_short_name()
        login_stat = False
    
    submittedValue = request.POST
    
    if bool(submittedValue):
        if 'categorySubmit' in submittedValue:
            category = submittedValue["categorySubmit"]
            if category == "All":
                allIngredient = allIngredient.all()
            else:
                categoryID = allIngredientCategory.get(ingredientCategoryName = category).ingredientCategoryID
                allIngredient = allIngredient.filter(ingredientCategory = categoryID)
        elif 'searchFor' in submittedValue:
            searchFor = submittedValue['searchFor']
            allIngredient = allIngredient.filter(ingredientName__contains = searchFor)
        
    template = loader.get_template('recipeManager/ingredient.html')
    
    context = {
        'loginStat' : login_stat,
        'name' : user_fname,
        'allIngredientCategory' : allIngredientCategory,
        'allIngredient' : allIngredient,
        'message' : message,
    }
    
    return HttpResponse(template.render(context, request))

########################################
#The function related to adding new Ingredient 
def newIngredient(request):
    message = ""
    allIngredientCategory = IngredientCategory.objects.all()
    
    user_fname = ', Guest'
    login_stat = True
    if request.user.is_authenticated:
        user_fname = ', ' + request.user.get_short_name()
        login_stat = False
    
        #This is what we get from user    
        if request.POST:
            name = request.POST['ingredientName']
            baseCal = request.POST['baseCalorie']
            category = request.POST['ingredientCategory']
            imageDir = request.POST['ingredientImg']
            
            if not isfloat(baseCal):
                message = "You entered the wrong value for Base Calorie!"
            else:
                newItem = Ingredient.objects.create(ingredientName = name,
                                                        baseCalorie = baseCal,
                                                        ingredientCategory = IngredientCategory.objects.get(ingredientCategoryName = category),
                                                        ingredientImg = imageDir)
                newItem.save()
                return redirect('ingredient') 
            
        template = loader.get_template('recipeManager/newIngredient.html')
        
        context = {
            'loginStat' : login_stat,
            'name' : user_fname,
            'allIngredientCategory' : allIngredientCategory,
            'message' : message,
        }
        
        return HttpResponse(template.render(context, request))
    else:
        return redirect('index') 

########################################
#This function is used to show all utensil 
def utensil(request):
    message = ""
    allUtensil = Utensil.objects.all()
    
    #Check the search request
    if request.POST:
        searchFor = request.POST['searchFor']
        allUtensil = allUtensil.filter(utensilName__contains=searchFor) 
    
    if not allUtensil:
        message = "There is no entry for utensil!!!"
    user_fname = ', Guest'
    login_stat = True
    if request.user.is_authenticated:
        user_fname = ', ' + request.user.get_short_name()
        login_stat = False
        
    template = loader.get_template('recipeManager/utensil.html')
    
    context = {
        'loginStat' : login_stat,
        'name' : user_fname,
        'allUtensil' : allUtensil,
        'message' : message,
    }
    
    return HttpResponse(template.render(context, request))

########################################
#This function is used to show all list
def userList(request):
    message = ""
    
    user_fname = ', Guest'
    login_stat = True
    if request.user.is_authenticated:
        user_fname = ', ' + request.user.get_short_name()
        login_stat = False
        
        template = loader.get_template('recipeManager/list.html')
        
        context = {
            'loginStat' : login_stat,
            'name' : user_fname,
            'message' : message,
        }
        
        return HttpResponse(template.render(context, request))
    else:
        return redirect('index') 

#################################################




############################################3
########################################
#Creating the login page 
def loginFunc(request):
    message = ""
    #This is what we get from user 
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            message = "Invalid Username or Password!!!"
    
    template = loader.get_template('recipeManager/login.html')
    context = {
        'message': message,
    }
    return HttpResponse(template.render(context, request))

########################################
#Logout function
def logoutFunc(request):
    logout(request)
    # Redirect to a success page.
    return redirect('index')

########################################
#Creating the registration page 
def register(request):
    message = ""
    allUser = User.objects.all()
    
    #This is what we get from user 
    if request.POST:
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
                
        if allUser.filter(username = username):
            message = "This username already exists!"
        elif allUser.filter(email = email):
            message ="This email address already exists!"
        else:
            person = User.objects.create_user(username, email, password,
                                          first_name = first_name, last_name = last_name)
            person.save()
            login(request, person)
            return redirect('index')
    
    template = loader.get_template('recipeManager/register.html')
    context = {
        'message': message,
    }
    return HttpResponse(template.render(context, request))

########################################
#Profile setting page
def profile(request):
    message = ""
    
    login_stat = True
    if request.user.is_authenticated:
        user_fname = ', ' + request.user.get_short_name()
        login_stat = False
         
        user = request.user
        userInfo = User.objects.filter(username = user)
        old_id = userInfo[0].id
        old_username = userInfo[0].username
        old_password = userInfo[0].password
        
        if request.POST:
            fname = request.POST['firstname']
            lname = request.POST['lastname']
            #username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            print(password)
            
            if User.objects.filter(email = email) and (User.objects.filter(email = email)[0].id != old_id): 
                message ="This email address already exists!"
            else: 
                if password:
                    new_info = User(id=old_id, username = old_username, email = email,
                                    first_name = fname, last_name = lname)
                    new_info.set_password(password)
                    
                else:
                    new_info = User(id=old_id, username = old_username, email = email, password = old_password,
                                    first_name = fname, last_name = lname)
                
                new_info.save()
                login(request, new_info)
                return redirect('index')
                
        
        template = loader.get_template('recipeManager/profile.html')
        
        context = {
            'loginStat' : login_stat,
            'name' : user_fname,
            'userInfo' : userInfo[0],
            'message' : message,
        }
        
        return HttpResponse(template.render(context, request))
    else:
        return redirect('index')


#############################################
#############################################
#Additional Functions
#############################################

#isfloat():
def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False
