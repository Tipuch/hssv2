from django.conf.urls import url, include
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    url(r'', views.index, name='index'),
    url(r'^add_new_category/', views.add_new_category, name='add_new_category'),

]
