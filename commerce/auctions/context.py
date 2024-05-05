class BidContext:
    auction_data = None
    highest_bid = None
    bid_data_list = None
    bid_form = None


class CommentContext:
    id_auction = None
    auction_comments_list = None
    new_comment_form = None


class AuctionContext(BidContext, CommentContext):
    auction_in_watchlist = None


class ResponseCommentContext:
    response_form = None
    comment = None
