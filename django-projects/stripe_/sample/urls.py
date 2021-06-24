from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('checkout', views.checkout, name='checkout'),
    path('create-checkout-session', views.create_checkout_session, name='create_checkout_session'),
    path('success', views.success, name='success'),
    path('cancel', views.cancel, name='cancel'),
]