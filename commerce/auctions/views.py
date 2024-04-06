from django.shortcuts import render

from auctions import util
from auctions.forms import BidForm
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
        user_bids = util.get_user_bids_made(auction_id=id_auction, bidder_user=request.user.id)
    auction_comments = util.get_auction_comments(auction_id=id_auction)
    return render(request, "auctions/auction_view.html", context={
        "user_data": request.user,
        "auction_data": requested_auction,
        "bid_data_list": user_bids,
        "highest_bid": util.get_max_bid(id_auction),
        "auction_comments": auction_comments,
        "bid_form": BidForm(initial={"auction_seller": requested_auction.seller_user.id,
                                     "auction": id_auction,
                                     "auction_initial_price": requested_auction.current_price})
    })


def new_bid(request, id_auction):
    bid_form_data = BidForm(request.POST)
    if bid_form_data.is_valid():
        valid_bid_data = bid_form_data.cleaned_data
        Bid.objects.create(
            auction_id_id=id_auction,
            bidder_user_id=request.user.id,
            offer_price=valid_bid_data.get("bid_value")
        )
        bid_form_data = BidForm(initial={**request.POST.dict(), "bid_value": None})
    updated_auction = Auction.objects.get(pk=id_auction)
    return render(request, "auctions/bids.html", context={
        "auction_data": updated_auction,
        "highest_bid": util.get_max_bid(id_auction),
        "bid_data_list": util.get_user_bids_made(auction_id=id_auction, bidder_user=request.user.id),
        "bid_form": bid_form_data
    })
