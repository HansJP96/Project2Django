from django import forms
from django.core.exceptions import ValidationError

from auctions.models import Auction
from auctions.utils import querys


class BidForm(forms.Form):
    auction = forms.CharField(widget=forms.HiddenInput())
    bid_value = forms.IntegerField(label=False)
    auction_initial_price = forms.CharField(widget=forms.HiddenInput())

    def clean(self):
        cleaned_data = super().clean()
        new_bid_value = cleaned_data.get("bid_value")
        id_auction = cleaned_data.get("auction")
        initial_auction_price = cleaned_data.get("auction_initial_price")
        highest_current_bid = querys.get_max_bid(id_auction)
        last_price = highest_current_bid.offer_price if highest_current_bid else int(initial_auction_price)
        if int(new_bid_value) <= last_price:
            raise ValidationError("The price less than or equal to the highest bid")
        return cleaned_data


class NewCommentForm(forms.Form):
    auction = forms.CharField(widget=forms.HiddenInput())
    comment = forms.CharField(label=False,
                              max_length=512,
                              widget=forms.Textarea(attrs={'placeholder': 'Add your comment...', 'maxlength': '512'}))


class ResponseCommentForm(forms.Form):
    id_comment = forms.CharField(widget=forms.HiddenInput())
    response = forms.CharField(label=False, max_length=256, widget=forms.Textarea(
        attrs={'placeholder': 'Add your response...', 'cols': 1, 'rows': 3, 'maxlength': '256'}))


class NewAuctionListingForm(forms.ModelForm):
    title = forms.CharField(max_length=100, widget=forms.TextInput)
    description = forms.CharField(max_length=256, widget=forms.Textarea(
        attrs={'placeholder': 'Add your description...', 'cols': 100, 'rows': 5, 'maxlength': '512'}))
    photo = forms.CharField(label="Photo link", required=False, widget=forms.TextInput)
    seller_user_id = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Auction
        fields = ["title", "description", "current_price", "photo", "category", "seller_user_id"]
