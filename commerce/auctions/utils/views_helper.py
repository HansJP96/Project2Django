from auctions.forms import ResponseCommentForm
from auctions.utils import querys


def update_auction_current_price_showed(auction_list):
    for auction_data in auction_list:
        highest_current_bid = auction_data.auction_bids.filter(auction=auction_data.id).order_by('-offer_price').first()
        auction_data.current_price = highest_current_bid.offer_price \
            if highest_current_bid else auction_data.current_price
    return auction_list

def auction_comments_factory(id_auction, comment_obj=None, response_form_obj=None):
    comment_data_response_form = []
    for comment in querys.get_auction_comments(id_auction=id_auction):
        if comment_obj != comment:
            response_form = ResponseCommentForm(initial={"auction": id_auction, "id_comment": comment.id})
            comment_data_response_form.append((comment, response_form))
        else:
            comment_data_response_form.append((comment_obj, response_form_obj))
    return comment_data_response_form
