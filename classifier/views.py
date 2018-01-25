from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest

from django.utils.translation import ugettext
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET

from .forms import CategoryForm, PhotoAssociationForm
from .constants import CATEGORIES_LIMIT, PHOTOS_DISPLAY_LIMIT
from .models import Category, PhotoSet


@ensure_csrf_cookie
@require_GET
def index(request):
    return render(
        request,
        'classifier/index.html',
        {'photo_sets': PhotoSet.objects.all()}
    )


class CategoriesView(View):
    template_name = 'classifier/categories.html'

    def get(self, request):
        if request.is_ajax():
            categories = Category.objects.all().annotate(photo_count=Count('gallery__photos'))
            return render(
                request, self.template_name, {
                    'categories': categories,
                    'CATEGORIES_LIMIT': CATEGORIES_LIMIT
                })
        else:
            return HttpResponseBadRequest(reason=ugettext("Request needs to be sent via AJAX"))

    def post(self, request):
        if request.is_ajax():
            category_form = CategoryForm(request.POST)
            if category_form.is_valid():
                category_form.save()
                return HttpResponse(status=201)
            else:
                return HttpResponseBadRequest(reason=str(category_form.errors))
        else:
            return HttpResponseBadRequest(reason=ugettext("Request needs to be sent via AJAX"))


class PhotosView(View):
    template_name = 'classifier/thumbnails_gallery.html'

    def get(self, request, photo_set_id):
        if request.is_ajax():
            photos = get_object_or_404(
                PhotoSet.objects.prefetch_related('gallery__photos'), id=photo_set_id).gallery.photos.all()
            # limit photos displayed
            photos = photos[:PHOTOS_DISPLAY_LIMIT]
            return render(request, self.template_name, {'photos': photos})
        else:
            return HttpResponseBadRequest(reason=ugettext("Request needs to be sent via AJAX"))


class PhotoAssociationView(View):

    def post(self, request):
        if request.is_ajax():
            association_form = PhotoAssociationForm(request.POST)
            if association_form.is_valid():
                association_form.associate_photo()
                return HttpResponse()
            else:
                return HttpResponseBadRequest(reason=str(association_form.errors))
        else:
            return HttpResponseBadRequest(reason=ugettext("Request needs to be sent via AJAX"))