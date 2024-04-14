class UserContext:
    user_data = None


class BidContext:
    id_auction = None
    highest_bid = None
    bid_data_list = None
    bid_form = None


class CommentContext(UserContext):
    id_auction = None
    auction_comments_list = None
    new_comment_form = None


class AuctionContext(BidContext, CommentContext):
    auction_data = None


class ResponseCommentContext(UserContext):
    response_form = None
    comment = None
