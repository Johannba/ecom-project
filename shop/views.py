from django.shortcuts import render
from .models import *

from django.http import JsonResponse

import json

# Create your views here.


def shop(request, *args, **kwargs):
    """vue des produits"""

    produits = Produit.objects.all()
    context = {"produits": produits}

    return render(request, "shop/index.html", context)


def panier(request, *args, **kwargs):
    if request.user.is_authenticated:
        client = request.user.client

        commande, created = Commande.objects.get_or_create(
            client=client, complete=False
        )

        arcticles = commande.commandearticle_set.all()

    else:
        arcticles = []

        commande = {"get_panier_total": 0, "get_panier_article": 0}

    context = {"arcticles": arcticles, "commande": commande}

    return render(request, "shop/panier.html", context)


def commande(request, *args, **kwargs):
    context = {}

    if request.user.is_authenticated:
        client = request.user.client

        commande, created = Commande.objects.get_or_create(
            client=client, complete=False
        )

        arcticles = commande.commandearticle_set.all()

    else:
        arcticles = []

        commande = {"get_panier_total": 0, "get_panier_article": 0}

    context = {"arcticles": arcticles, "commande": commande}

    return render(request, "shop/commande.html", context)


def update_arcticle(request, *arg, **kwarg):
    data = json.loads(request.body)
    produit_id = data["produit_id"]
    action = data["action"]
    print(action, produit_id)
    return JsonResponse("produit modifier", safe=False)
