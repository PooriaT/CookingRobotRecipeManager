from django.contrib import admin

from .models import UserProfile
from .models import Recipe
from .models import List
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Recipe)
admin.site.register(List)
