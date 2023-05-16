from django.shortcuts import render
from .models import *

# Create your views here.


def shop(request, *args, **kwargs):
    """vue des produits"""

    produits = Produit.objects.all()
    context = {"produits": produits}

    return render(request, "shop/index.html", context)


def panier(request, *args, **kwargs):
    context = {}

    return render(request, "shop/panier.html", context)


def commande(request, *args, **kwargs):
    context = {}

    return render(request, "shop/commande.html", context)
