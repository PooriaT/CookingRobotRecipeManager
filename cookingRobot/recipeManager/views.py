from django.shortcuts import render
from django.template import loader

from django.http import HttpResponse

from .models import UserProfile
from .models import Recipe
from .models import List

def index(request):
    
    allObjs = Recipe.objects.all()
    sortType = request.POST
    
    print(sortType["sort"])
    if sortType["sort"] != 'default' and sortType["sort"] != ' ':
        allObjs = sortByItem(sortType["sort"], allObjs)
        
    
    template = loader.get_template('recipeManager/index.html')
    context = {
        'items': allObjs,
    }
    
    return HttpResponse(template.render(context, request))

def sortByItem(item, allItems):
    allItems = allItems.order_by(item)
    return allItems

def searchItem(request):
    pass