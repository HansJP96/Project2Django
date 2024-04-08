from auctions.forms import ResponseCommentForm
from auctions.utils import querys


def auction_comments_factory(id_auction, comment_obj=None, response_form_obj=None):
    comment_data_response_form = []
    for comment in querys.get_auction_comments(id_auction=id_auction):
        if comment_obj != comment:
            response_form = ResponseCommentForm(initial={"auction": id_auction, "id_comment": comment.id})
            comment_data_response_form.append((comment, response_form))
        else:
            comment_data_response_form.append((comment_obj, response_form_obj))
    return comment_data_response_form
