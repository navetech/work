from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("unregister", views.unregister_view, name="unregister"),
    path("menu", views.menu, name="menu"),
    path('item_order/<flavor_id>/<size_id>', views.item_order, name="item_order"),
    path('shopping_cart', views.shopping_cart, name="shopping_cart"),
    path('checkout', views.checkout, name="checkout"),
    path('create_checkout_session', views.create_checkout_session, name="create_checkout_session"),
    ]
