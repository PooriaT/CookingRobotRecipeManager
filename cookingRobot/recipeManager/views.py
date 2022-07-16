from django.shortcuts import render
from django.template import loader

from django.http import HttpResponse

from .models import UserProfile
from .models import Recipe
from .models import List

def index(request):
    
    obj = Recipe.objects.all()
    #output="test"
    template = loader.get_template('recipeManager/index.html')
    context = {
        'obj': obj,
    }
    return HttpResponse(template.render(context, request))
    #return HttpResponse(output)