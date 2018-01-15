from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
import json
from photologue.models import Photo, Gallery
from .models import Categorie


def index(request):
    extra_content = {}

    galleries = Gallery.objects.all()
    categories = Categorie.objects.all()


    extra_content['galleries'] = galleries
    extra_content['categories'] = categories

    return render(
        request,
        'classifier/index.html',
        extra_content
    )


# def get_new_picture(request):


def post_category(request):
    response_data = {}
    response_data['something'] = 'useful'
    return HttpResponse(json.dumps({'success': False, 'cause': None}), content_type='application/json')


# This function add a new category to the list if there's no more than 8 of them.
def add_new_category(request):
    catname = request.GET.get('catname') 
    c1 = Categorie(title=catname)
    if Categorie.objects.all() < 8:
        c1.save()
        return JsonResponse(data)
        
    else:
        return HttpResponse("There's already 8 categories, which is the maximum you can have.")
