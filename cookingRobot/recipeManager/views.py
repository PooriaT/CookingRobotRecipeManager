from django.shortcuts import render, redirect
from django.template import loader

from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .models import IngredientCategory
from .models import Ingredient
from .models import Utensil
from .models import Recipe
from .models import RecipeCategory
from .models import List

########################################
#Homepage 
def index(request):
    allObjs = {}#Recipe.objects.all()
    
    user_fname = ', Guest'
    login_stat = True
    if request.user.is_authenticated:
        user_fname = ', ' + request.user.get_short_name()
        login_stat = False
    
    submittedValue = request.POST
    
    if bool(submittedValue):
        if 'sortSubmit' in submittedValue:
            if submittedValue["sort"] != 'default':
                item = submittedValue["sort"]
                allObjs = sortByItem(item, allObjs)
        elif 'searchSubmit' in submittedValue:
            item = submittedValue['search']
            searchFor = submittedValue['searchFor']
            allObjs = searchItem(item, searchFor, allObjs)
        
    
    template = loader.get_template('recipeManager/index.html')
    
    context = {
        'loginStat' : login_stat,
        'name' : user_fname,
        'items': allObjs,
    }
    
    return HttpResponse(template.render(context, request))

########################################
#The function related to adding new Ingredient 
def newRecipe(request):
    message = "I am an empty new recipe page!!!!!!!!!!!"
    user_fname = ', Guest'
    login_stat = True
    if request.user.is_authenticated:
        user_fname = ', ' + request.user.get_short_name()
        login_stat = False
    template = loader.get_template('recipeManager/newRecipe.html')
    
    context = {
        'loginStat' : login_stat,
        'name' : user_fname,
        'message' : message,
    }
    
    return HttpResponse(template.render(context, request))
    

########################################
#Query for Ingredients
def ingredient(request):
    message = "I am empty!!!!!!!!!!!1"
    user_fname = ', Guest'
    login_stat = True
    if request.user.is_authenticated:
        user_fname = ', ' + request.user.get_short_name()
        login_stat = False
    template = loader.get_template('recipeManager/ingredient.html')
    
    context = {
        'loginStat' : login_stat,
        'name' : user_fname,
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
        print(request.POST)
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

#################################################
########################################
#This is the sorting function to re order the data illustration
def sortByItem(item, allItems):
    allItems = allItems.order_by(item)
    return allItems

########################################
#This is the searching function
def searchItem(item, searchFor, allItems):
    if item == "recipeName":
        allItems = allItems.filter(recipeName=searchFor)
    elif item == "category":
        allItems = allItems.filter(category=searchFor)
    elif item == "chefName":
        allItems = allItems.filter(chefName=searchFor)
    else:
        allItems = {}
    
    return allItems



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
        print(user)
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
            message =" This email address already exists!"
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
