from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ahmed', views.ahmed, name='ahmed'),
    path("<str:name>", views.greet, name='greet')
]