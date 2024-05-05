from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy


class Category(models.IntegerChoices):
    UNCATEGORIZED = 1001, gettext_lazy("Uncategorized")
    FASHION = 0, gettext_lazy("Fashion")
    TOYS = 1, gettext_lazy("Toys")
    HOME_GARDEN = 2, gettext_lazy("Home & Garden")
    MUSIC = 3, gettext_lazy("Music")
    BOOKS = 4, gettext_lazy("Books & Magazines")
    COMPUTERS_TABLETS = 5, gettext_lazy("Computers/Tablets")
    VIDEOGAMES = 6, gettext_lazy("Video Games & Consoles")


class Auction(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=512)
    current_price = models.IntegerField()
    photo = models.CharField(max_length=512, blank=True)
    category = models.IntegerField(choices=Category, blank=True, default=Category.UNCATEGORIZED)
    seller_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="creator")
    is_closed = models.BooleanField(default=False)
    create_date = models.DateTimeField(default=timezone.now, editable=False)


class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.PROTECT, related_name="auction_bids")
    bidder_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, related_name="user_bids")
    offer_price = models.IntegerField()
    update_time = models.DateTimeField(default=timezone.now, editable=False)


class Comment(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="auction_comments")
    client_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, related_name="client")
    comment = models.TextField(max_length=512)
    response = models.TextField(max_length=256, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
