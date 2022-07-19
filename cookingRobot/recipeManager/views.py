from django.shortcuts import render
from django.template import loader

from django.http import HttpResponse

from .models import UserProfile
from .models import Recipe
from .models import List


def index(request):
    allObjs = Recipe.objects.all()
    
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
        'items': allObjs,
    }
    
    return HttpResponse(template.render(context, request))

#This is the sorting function to re order the data illustration
def sortByItem(item, allItems):
    allItems = allItems.order_by(item)
    return allItems

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