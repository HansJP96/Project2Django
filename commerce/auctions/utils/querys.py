from auctions.models import Bid, Comment


def get_all_auction_bids(id_auction):
    return Bid.objects.filter(auction=id_auction).order_by('-update_time')

def get_user_bids_made(id_auction, bidder_user):
    return Bid.objects.filter(auction=id_auction, bidder_user=bidder_user).order_by('-update_time')


def get_max_bid(id_auction):
    return Bid.objects.filter(auction=id_auction).order_by('-offer_price').first()


def get_auction_comments(id_auction):
    return Comment.objects.filter(auction=id_auction).order_by('-create_date')
