from django.contrib import admin


from .models import IngredientCategory
from .models import Ingredient
from .models import Utensil
from .models import Recipe
from .models import RecipeCategory
from .models import List


# Register your models here.
admin.site.register(IngredientCategory)
admin.site.register(Ingredient)
admin.site.register(Utensil)
admin.site.register(Recipe)
admin.site.register(RecipeCategory)
admin.site.register(List)