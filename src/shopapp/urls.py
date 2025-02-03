from django.urls import path

from . import views

urlpatterns = [
    path("", views.indexView, name="index"),
    path("login/", views.loginView, name="login"),
    path("register/", views.registerView, name="register"),
    path("products/", views.productsView, name="products"),
    path("products/<int:product_id>/", views.productDetailView, name='productDetail'),
    path("account/", views.accountView, name="account"),
    path("cart/", views.cartView, name="cart"),
    path("checkout/", views.checkoutView, name="checkout"),
    path('transaction-history/', views.transactionHistoryView, name='transactionHistory'),
    path("logout/", views.logoutView, name="logout"),
]