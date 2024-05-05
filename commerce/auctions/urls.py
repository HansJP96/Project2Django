from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("listings/<int:id_auction>", views.auction, name="auction"),
    path("listings/<int:id_auction>/add-bid", views.new_bid, name="new_bid"),
    path("listings/<int:id_auction>/new-comment", views.new_comment, name="new_comment"),
    path("listings/response-comment/<int:id_comment>", views.response_comment, name="response_comment"),
    path("create-listing", views.create_auction_listing, name="create_listing"),
    path("auction-current-price/<int:id_auction>", views.current_price, name="current_price"),
    path("watchlist", views.view_watchlist, name="view_watchlist"),
    path("watchlist/action/<int:id_auction>/<str:auction_in_watchlist>", views.add_remove_auction_watchlist,
         name="watchlist_action"),
    path("watchlist/update", views.update_watchlist_count, name="watchlist_update"),
    path("categories", views.show_all_categories, name="category_list"),
    path("categories/<int:category_value>", views.auction_by_category, name="category_auction"),
    path("close-auction/<int:id_auction>", views.close_auction, name="close_auction")
]
