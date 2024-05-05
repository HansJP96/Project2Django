from django.contrib.auth.models import AbstractUser
from django.db import models

from auctions.models import Auction


# Create your models here.
class User(AbstractUser):
    watchlist = models.ManyToManyField(Auction, related_name="followed_auctions")
