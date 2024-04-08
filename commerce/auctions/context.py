class AuctionContext:
    user_data = None
    auction_data = None
    highest_bid = None
    bid_data_list = None
    auction_comments_list = None
    bid_form = None
    new_comment_form = None


class BidContext:
    id_auction = None
    highest_bid = None
    bid_data_list = None
    auction_comments_list = None
    bid_form = None


class CommentContext:
    id_auction = None
    user_data = None
    auction_comments_list = None
    new_comment_form = None
