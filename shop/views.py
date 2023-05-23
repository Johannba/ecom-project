from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import *
from datetime import datetime


import json

# Create your views here.


def shop(request, *args, **kwargs):
    """vue des produits"""

    produits = Produit.objects.all()
    if request.user.is_authenticated:
        client = request.user.client

        commande, created = Commande.objects.get_or_create(
            client=client, complete=False
        )

        nombre_arcticle = commande.get_panier_article

    else:
        arcticles = []

        commande = {"get_panier_total": 0, "get_panier_article": 0}
        nombre_arcticle = commande["get_panier_article"]

    context = {
        "nombre_arcticle": nombre_arcticle,
        "produits": produits,
    }

    return render(request, "shop/index.html", context)


def panier(request, *args, **kwargs):
    if request.user.is_authenticated:
        client = request.user.client

        commande, created = Commande.objects.get_or_create(
            client=client, complete=False
        )

        arcticles = commande.commandearticle_set.all()
        nombre_arcticle = commande.get_panier_article

    else:
        arcticles = []

        commande = {"get_panier_total": 0, "get_panier_article": 0}

        nombre_arcticle = commande["get_panier_article"]

    context = {
        "arcticles": arcticles,
        "commande": commande,
        "nombre_arcticle": nombre_arcticle,
    }

    return render(request, "shop/panier.html", context)


def commande(request, *args, **kwargs):
    if request.user.is_authenticated:
        client = request.user.client

        commande, created = Commande.objects.get_or_create(
            client=client, complete=False
        )

        arcticles = commande.commandearticle_set.all()

        nombre_arcticle = commande.get_panier_article

    else:
        arcticles = []

        commande = {"get_panier_total": 0, "get_panier_article": 0}
        nombre_arcticle = commande["get_panier_article"]

    context = {
        "arcticles": arcticles,
        "commande": commande,
        "nombre_arcticle": nombre_arcticle,
    }

    return render(request, "shop/commande.html", context)


@login_required()
def update_arcticle(request, *arg, **kwarg):
    data = json.loads(request.body)
    produit_id = data["produit_id"]
    action = data["action"]
    client = request.user.client
    produit = Produit.objects.get(id=produit_id)

    commande, created = Commande.objects.get_or_create(client=client, complete=False)

    commande_arcticle, created = CommandeArticle.objects.get_or_create(
        commande=commande, produit=produit
    )

    if action == "add":
        commande_arcticle.quantite += 1
    if action == "remove":
        commande_arcticle.quantite -= 1

    commande_arcticle.save()

    if commande_arcticle.quantite <= 0:
        commande_arcticle.delete()

        return JsonResponse("produit ajoutés", safe=False)

    if request.user.is_authenticated:
        client = request.user.client
        commande, created = Commande.objects.get_or_create(
            client=client, complete=False
        )
        articles = commande.commandearticle_set.all()
        nombre_article = commande.get_panier_article
    else:
        articles = []
        commande = {"get_panier_total": 0, "get_panier_article": 0}

        nombre_article = commande["get_panier_article"]


def traitement_commande(request, *args, **kwargs):
    data = json.loads(request.body)
    print(data)

    transaction_id = datetime.now().timestamp()

    if request.user.is_authenticated:
        client = request.user.client
        commande, created = Commande.objects.get_or_create(
            client=client, complete=False
        )

        total = float(data["form"]["total"])

        commande.transaction_id = transaction_id

        if commande.get_panier_total == total:
            commande.complete = True

        commande.save()

        if commande.produit_physique:
            AddressChipping.objects.create(
                client=client,
                commande=commande,
                addresse=data["shipping"]["address"],
                city=data["shipping"]["city"],
                zipcode=data["shipping"]["zipcode"],
            )
        else:
            print("utilisateur non authentifié")
    return JsonResponse("Traiment complete", safe=False)
