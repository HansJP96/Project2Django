from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy

from users.models import User


class Category(models.IntegerChoices):
    FASHION = 0, gettext_lazy("Fashion")
    TOYS = 1, gettext_lazy("Toys")
    HOME_GARDEN = 2, gettext_lazy("Home & Garden")
    MUSIC = 3, gettext_lazy("Music")
    BOOKS = 4, gettext_lazy("Books & Magazines")
    COMPUTERS_TABLETS = 5, gettext_lazy("Computers/Tablets")
    VIDEOGAMES = 6, gettext_lazy("Video Games & Consoles")

    __empty__ = gettext_lazy("uncategorized")


class Auction(models.Model):
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=256)
    current_price = models.IntegerField()
    photo = models.CharField(max_length=256)
    category = models.IntegerField(choices=Category)
    create_date = models.DateTimeField(default=timezone.now, editable=False)
    seller_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator")


class Bid(models.Model):
    auction_id = models.ForeignKey(Auction, on_delete=models.PROTECT)
    creator_user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="auctioneer")
    bidder_user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="bidder")
    offer_price = models.IntegerField()
    update_time = models.DateTimeField(default=timezone.now, editable=False)

    def is_valid_bid(self, last_price):
        return int(self.offer_price) > last_price


class Comment(models.Model):
    auction_id = models.ForeignKey(Auction, on_delete=models.CASCADE)
    creator_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller")
    client_user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="client")
    comment = models.TextField()
    response = models.TextField(null=True)
    create_date = models.DateTimeField(default=timezone.now, editable=False)
