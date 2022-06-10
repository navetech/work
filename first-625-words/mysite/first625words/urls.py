from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('phrase/<phrase_id>', views.phrase, name='phrase'),
]
