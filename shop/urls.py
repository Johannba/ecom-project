from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path("", views.shop, name="shop"),
    path("panier/", views.panier, name="panier"),
    path("commande/", views.commande, name="commande"),
    path("update_arcticle/", views.update_arcticle, name="update_arcticle"),
]
