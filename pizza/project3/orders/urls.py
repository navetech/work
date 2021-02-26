from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("unregister", views.unregister_view, name="unregister"),
    path("menu", views.menu, name="menu"),
    path('flavor/<int:dish_id>/<int:type_id>/<int:flavor_id>', views.flavor_view, name="flavor"),
]