from django.shortcuts import render, redirect
from django.template import loader

from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .models import Recipe
from .models import List


def index(request):
    allObjs = Recipe.objects.all()
    
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

########################################
#Creating the login page 
def loginFunc(request):
    message = ""
    if request.POST:
        print(request.POST)
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
