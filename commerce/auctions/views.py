from django.http import HttpResponseBadRequest
from django.shortcuts import render

from auctions import util_bid
from auctions.models import Auction, Bid


def index(request):
    all_auctions = Auction.objects.all()
    for auction_data in all_auctions:
        highest_current_bid = auction_data.bid_set.filter(auction_id=auction_data.id).order_by('-offer_price').first()
        auction_data.current_price = highest_current_bid.offer_price \
            if highest_current_bid else auction_data.current_price
    return render(request, "auctions/index.html", context={
        "auctions_list": all_auctions
    })


def auction(request, id_auction):
    requested_auction = Auction.objects.get(pk=id_auction)
    user_bids = None
    is_user_authenticated = request.user.is_authenticated
    if is_user_authenticated:
        user_bids = util_bid.get_user_bids_made(auction_id=id_auction, bidder_user=request.user.id)
    return render(request, "auctions/auction_view.html", context={
        "user_data": request.user,
        "auction_data": requested_auction,
        "bid_data_list": user_bids,
        "highest_bid": util_bid.get_max_bid(id_auction)
    })


def new_bid(request, id_auction):
    new_bid_value = request.POST.get("bid-value")
    auctioneer_id = request.POST.get("auction-seller")
    initial_auction_price = request.POST.get("auction-initial_price")
    created_bid = Bid(offer_price=new_bid_value)
    highest_current_bid = util_bid.get_max_bid(id_auction)
    last_price = highest_current_bid.offer_price if highest_current_bid else int(initial_auction_price)
    if not created_bid.is_valid_bid(last_price):
        #TODO: REVISAR COMO AGREGAR LA VALIDACION EN EL HTML YA SEA CON FORM U OTRA COSA
        return HttpResponseBadRequest()
    created_bid.auction_id_id = id_auction
    created_bid.creator_user_id = auctioneer_id
    created_bid.bidder_user_id = request.user.id
    created_bid.save()
    return render(request, "auctions/bids.html", context={
        "auction_data": created_bid.auction_id,
        "bid_data_list": util_bid.get_user_bids_made(auction_id=id_auction, bidder_user=request.user.id)
    })
