from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('phrase/<phrase_id>', views.phrase, name='phrase'),
    path('select_target_languages', views.select_target_languages, name='select_target_languages'),
    path('put_target_languages', views.put_target_languages, name='put_target_languages'),
]
