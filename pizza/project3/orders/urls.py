from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("unregister", views.unregister_view, name="unregister"),
    path("menu", views.menu, name="menu"),
    path(
        "select-language/<language_id>", views.select_language,
        name="select_language"
    ),
    path(
        "select-currency/<currency_id>", views.select_currency,
        name="select_currency"
    ),
    path(
        "order/<dish_id>/<type_id>/<flavor_id>/<size_id>", views.order,
        name="order"
    ),
    path("shopping-cart", views.shopping_cart, name="shopping_cart"),
    path('checkout', views.checkout, name='checkout'),
    path(
        'create-checkout-session',
        views.create_checkout_session, name='create_checkout_session'
    ),
    path('success', views.success, name='success'),
    path('cancel', views.cancel, name='cancel'),
]
