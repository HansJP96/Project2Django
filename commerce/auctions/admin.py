from django.contrib import admin

from .models import Auction, Comment, Bid

# Register your models here.
admin.site.register(Auction)
admin.site.register(Bid)
admin.site.register(Comment)
