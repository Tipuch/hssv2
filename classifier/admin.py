from django.contrib import admin
from .models import Categorie

class CategorieAdmin(admin.ModelAdmin):
    pass
admin.site.register(Categorie, CategorieAdmin)

# Register your models here.
