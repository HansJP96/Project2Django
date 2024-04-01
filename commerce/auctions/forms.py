from django import forms
from django.core.exceptions import ValidationError

from auctions import util_bid


class BidForm(forms.Form):
    auction = forms.CharField(widget=forms.HiddenInput())
    bid_value = forms.IntegerField(label=False)
    auction_seller = forms.CharField(widget=forms.HiddenInput())
    auction_initial_price = forms.CharField(widget=forms.HiddenInput())

    def clean(self):
        cleaned_data = super().clean()
        new_bid_value = cleaned_data.get("bid_value")
        id_auction = cleaned_data.get("auction")
        initial_auction_price = cleaned_data.get("auction_initial_price")
        highest_current_bid = util_bid.get_max_bid(id_auction)
        last_price = highest_current_bid.offer_price if highest_current_bid else int(initial_auction_price)
        if int(new_bid_value) <= last_price:
            raise ValidationError("The price is lower than the last bid")
        return cleaned_data
