from django.shortcuts import render

from auctions.context import AuctionContext, BidContext, CommentContext, ResponseCommentContext
from auctions.forms import BidForm, NewCommentForm, ResponseCommentForm, NewAuctionListingForm
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
    auction_context = AuctionContext()
    auction_context.user_data = request.user
    auction_context.auction_data = Auction.objects.get(pk=id_auction)
    is_user_authenticated = request.user.is_authenticated
    if is_user_authenticated:
        auction_context.bid_data_list = querys.get_user_bids_made(id_auction=id_auction, bidder_user=request.user.id)
    auction_context.highest_bid = querys.get_max_bid(id_auction)
    auction_context.bid_form = BidForm(
        initial={"auction": id_auction, "auction_initial_price": auction_context.auction_data.current_price})
    auction_context.new_comment_form = NewCommentForm(initial={"auction": id_auction})
    auction_context.auction_comments_list = views_helper.auction_comments_factory(id_auction=id_auction)
    return render(request, "auctions/auction_view.html", context=vars(auction_context))


def new_bid(request, id_auction):
    bid_context = BidContext()
    bid_context.id_auction = id_auction
    bid_form_data = BidForm(request.POST)
    if bid_form_data.is_valid():
        valid_bid_data = bid_form_data.cleaned_data
        Bid.objects.create(
            auction_id=id_auction,
            bidder_user_id=request.user.id,
            offer_price=valid_bid_data.get("bid_value")
        )
        bid_form_data = BidForm(initial={**request.POST.dict(), "bid_value": None})
    bid_context.highest_bid = querys.get_max_bid(id_auction)
    bid_context.bid_data_list = querys.get_user_bids_made(id_auction=id_auction, bidder_user=request.user.id)
    bid_context.bid_form = bid_form_data
    return render(request, "auctions/bids.html", context=vars(bid_context))


def new_comment(request, id_auction):
    comment_context = CommentContext()
    comment_context.id_auction = id_auction
    new_comment_form_data = NewCommentForm(request.POST)
    if new_comment_form_data.is_valid():
        valid_comment_data = new_comment_form_data.cleaned_data
        Comment.objects.create(
            auction_id=id_auction,
            client_user_id=request.user.id,
            comment=valid_comment_data.get("comment")
        )
        new_comment_form_data = NewCommentForm(initial={**request.POST.dict(), "comment": None})
    comment_context.user_data = request.user
    comment_context.auction_comments_list = views_helper.auction_comments_factory(id_auction=id_auction)
    comment_context.new_comment_form = new_comment_form_data
    return render(request, "auctions/comments/comments.html", context=vars(comment_context))


def response_comment(request, id_comment):
    response_context = ResponseCommentContext()
    response_context.user_data = request.user
    comment_response_form_data = ResponseCommentForm(request.POST)
    comment = Comment.objects.get(pk=id_comment)
    if comment_response_form_data.is_valid():
        valid_comment_data = comment_response_form_data.cleaned_data
        comment.response = valid_comment_data.get("response")
        comment.save()
        response_context.comment = comment
    else:
        response_context.response_form = comment_response_form_data
    return render(request, "auctions/comments/comment_response.html", context=vars(response_context))


def create_auction_listing(request):
    auction_listing_form = NewAuctionListingForm()
    return render(request, "auctions/new_listing.html", context={"form": auction_listing_form})
