from django.conf.urls import url
from django.urls import path

from . import views

app_name = "classifier"

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^categories/$', views.CategoriesView.as_view(), name='categories'),
    path('photos/<int:photo_set_id>/', views.PhotosView.as_view(), name='photos'),
    path('photos/associate/', views.PhotoAssociationView.as_view(), name='associate_photo')
]
