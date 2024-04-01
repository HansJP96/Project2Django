from auctions.models import Bid


def get_user_bids_made(auction_id, bidder_user):
    return Bid.objects.filter(auction_id=auction_id, bidder_user=bidder_user).order_by('-update_time')


def get_max_bid(auction_id):
    return Bid.objects.filter(auction_id=auction_id).order_by('-offer_price').first()
