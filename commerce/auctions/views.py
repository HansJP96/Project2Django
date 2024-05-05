from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from auctions.context import AuctionContext, BidContext, CommentContext, ResponseCommentContext
from auctions.forms import BidForm, NewCommentForm, ResponseCommentForm, NewAuctionListingForm
from auctions.models import Auction, Bid, Comment, Category
from auctions.utils import querys, views_helper


def index(request):
    all_auctions = views_helper.update_auction_current_price_showed(Auction.objects.all())
    return render(request, "auctions/index.html", context={
        "auctions_list": all_auctions
    })


def auction(request, id_auction):
    auction_context = AuctionContext()
    auction_context.auction_data = Auction.objects.get(pk=id_auction)
    is_user_authenticated = request.user.is_authenticated
    if is_user_authenticated:
        auction_context.bid_data_list = querys.get_all_auction_bids(id_auction) \
            if request.user == auction_context.auction_data.seller_user \
            else querys.get_user_bids_made(id_auction=id_auction, bidder_user=request.user.id)
        auction_context.auction_in_watchlist = auction_context.auction_data in request.user.watchlist.all()
    auction_context.highest_bid = querys.get_max_bid(id_auction)
    auction_context.bid_form = BidForm(
        initial={"auction": id_auction, "auction_initial_price": auction_context.auction_data.current_price})
    auction_context.new_comment_form = NewCommentForm(initial={"auction": id_auction})
    auction_context.auction_comments_list = views_helper.auction_comments_factory(id_auction=id_auction)
    print(auction_context.auction_data.create_date)
    return render(request, "auctions/auction_view.html", context=vars(auction_context))


def new_bid(request, id_auction):
    bid_context = BidContext()
    bid_context.auction_data = Auction.objects.get(pk=id_auction)
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


def current_price(request, id_auction):
    auction_bid_price = querys.get_max_bid(id_auction)
    return render(request, "auctions/partial/current_price.html", context={
        "highest_bid": auction_bid_price,
        "auction_data": auction_bid_price.auction,
    })


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
    comment_context.auction_comments_list = views_helper.auction_comments_factory(id_auction=id_auction)
    comment_context.new_comment_form = new_comment_form_data
    return render(request, "auctions/comments/comments.html", context=vars(comment_context))


def response_comment(request, id_comment):
    response_context = ResponseCommentContext()
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
    is_auction_created = False
    if request.method == "POST":
        new_auction_form = NewAuctionListingForm({**request.POST.dict(), "seller_user_id": request.user.id})
        if new_auction_form.is_valid():
            valid_new_auction = new_auction_form.cleaned_data
            Auction.objects.create(
                title=valid_new_auction.get("title"),
                description=valid_new_auction.get("description"),
                current_price=valid_new_auction.get("current_price"),
                photo=valid_new_auction.get("photo"),
                category=valid_new_auction.get("category"),
                seller_user_id=valid_new_auction.get("seller_user_id")
            )
            is_auction_created = True
        else:
            return render(request, "auctions/new_listing.html",
                          context={"new_auction_form": new_auction_form, "is_created": is_auction_created})
    return render(request, "auctions/new_listing.html",
                  context={"new_auction_form": NewAuctionListingForm(), "is_created": is_auction_created})


def view_watchlist(request):
    watchlist_list = views_helper.update_auction_current_price_showed(request.user.watchlist.all()) or []
    return render(request, "auctions/index.html", context={
        "auctions_list": watchlist_list
    })


def add_remove_auction_watchlist(request, id_auction, auction_in_watchlist):
    if auction_in_watchlist == "True":
        request.user.watchlist.remove(id_auction)
    elif auction_in_watchlist == "False":
        request.user.watchlist.add(id_auction)
    else:
        return HttpResponse(status=400)
    auction_context = AuctionContext()
    auction_context.auction_data = Auction.objects.get(pk=id_auction)
    auction_context.auction_in_watchlist = auction_context.auction_data in request.user.watchlist.all()
    return render(request, "auctions/partial/watchlist_button.html", context=vars(auction_context))


def update_watchlist_count(request):
    return render(request, "auctions/partial/watchlist_count.html")


def show_all_categories(request):
    return render(request, "auctions/categories.html", context={
        "category_list": Category
    })


def auction_by_category(request, category_value):
    all_auctions_by_category = views_helper.update_auction_current_price_showed(
        Auction.objects.filter(category=category_value))
    return render(request, "auctions/index.html", context={
        "auctions_list": all_auctions_by_category,
        "category": Category(value=category_value).label
    })


def close_auction(request, id_auction):
    auction_to_close = Auction.objects.get(pk=id_auction)
    auction_to_close.is_closed = True
    auction_to_close.save()
    return HttpResponseRedirect(reverse("auction", kwargs={'id_auction': id_auction}))
