from django.shortcuts import render


def index(request):
    return render(request, "auctions/index.html")


def auction(request, id_auction):
    return render(request, "auctions/auction_view.html")
