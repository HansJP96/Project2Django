from auctions.forms import ResponseCommentForm
from auctions.utils import querys


def auction_comments_factory(id_auction, comment_obj=None, form_obj=None):
    forms = []
    for comment in querys.get_auction_comments(id_auction=id_auction):
        if comment_obj != comment:
            form = ResponseCommentForm(initial={"auction": id_auction, "id_comment": comment.id})
            forms.append((comment, form))
        else:
            forms.append((comment_obj, form_obj))
    return forms
