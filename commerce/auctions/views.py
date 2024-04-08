from django.shortcuts import render

from auctions.context import AuctionContext
from auctions.forms import BidForm, NewCommentForm, ResponseCommentForm
from auctions.models import Auction, Bid, Comment
from auctions.utils import querys, views_helper


def index(request):
    all_auctions = Auction.objects.all()
    for auction_data in all_auctions:
        highest_current_bid = auction_data.auction_bids.filter(auction=auction_data.id).order_by('-offer_price').first()
        auction_data.current_price = highest_current_bid.offer_price \
            if highest_current_bid else auction_data.current_price
    return render(request, "auctions/index.html", context={
        "auctions_list": all_auctions
    })


def auction(request, id_auction):
    requested_auction = Auction.objects.get(pk=id_auction)
    context = AuctionContext()
    context.user_data = request.user
    context.auction_data = requested_auction
    is_user_authenticated = request.user.is_authenticated
    if is_user_authenticated:
        context.bid_data_list = querys.get_user_bids_made(id_auction=id_auction, bidder_user=request.user.id)
    context.highest_bid = querys.get_max_bid(id_auction)
    context.bid_form = BidForm(
        initial={"auction": id_auction, "auction_initial_price": requested_auction.current_price})
    context.new_comment_form = NewCommentForm(initial={"auction": id_auction})
    context.auction_comments_list = views_helper.auction_comments_factory(id_auction=id_auction)
    return render(request, "auctions/auction_view.html", context=vars(context))


def new_bid(request, id_auction):
    bid_form_data = BidForm(request.POST)
    if bid_form_data.is_valid():
        valid_bid_data = bid_form_data.cleaned_data
        Bid.objects.create(
            auction_id=id_auction,
            bidder_user_id=request.user.id,
            offer_price=valid_bid_data.get("bid_value")
        )
        bid_form_data = BidForm(initial={**request.POST.dict(), "bid_value": None})
    return render(request, "auctions/bids.html", context={
        "id_auction": id_auction,
        "highest_bid": querys.get_max_bid(id_auction),
        "bid_data_list": querys.get_user_bids_made(id_auction=id_auction, bidder_user=request.user.id),
        "bid_form": bid_form_data
    })


def new_comment(request, id_auction):
    new_comment_form_data = NewCommentForm(request.POST)
    if new_comment_form_data.is_valid():
        valid_comment_data = new_comment_form_data.cleaned_data
        Comment.objects.create(
            auction_id=id_auction,
            client_user_id=request.user.id,
            comment=valid_comment_data.get("comment")
        )
        new_comment_form_data = NewCommentForm(initial={**request.POST.dict(), "comment": None})
    return render(request, "auctions/comments/comments.html", context={
        "id_auction": id_auction,
        "user_data": request.user,
        "auction_comments_list": views_helper.auction_comments_factory(id_auction=id_auction),
        "new_comment_form": new_comment_form_data
    })


def response_comment(request, id_comment):
    comment_response_form_data = ResponseCommentForm(request.POST)
    comment = Comment.objects.get(pk=id_comment)
    if comment_response_form_data.is_valid():
        valid_comment_data = comment_response_form_data.cleaned_data
        comment.response = valid_comment_data.get("response")
        comment.save()
    else:
        return render(request, "auctions/comments/comment_response.html", context={
            "user_data": request.user,
            "auction_comments_list": views_helper.auction_comments_factory(id_auction=comment.auction.id,
                                                                           comment_obj=comment,
                                                                           form_obj=comment_response_form_data)
        })
    return render(request, "auctions/comments/comment_response.html", context={
        "user_data": request.user,
        "comment": comment
    })
