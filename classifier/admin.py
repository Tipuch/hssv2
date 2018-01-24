from django.contrib import admin

from .models import Category, PhotoSet


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(PhotoSet)
class PhotoSetAdmin(admin.ModelAdmin):
    pass
