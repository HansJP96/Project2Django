from django.contrib import admin

from users.models import User


class UserWatchListAuctions(admin.ModelAdmin):
    model = User
    filter_horizontal = ('watchlist',)


# Register your models here.
admin.site.register(User, UserWatchListAuctions)
