from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("listings/<int:id_auction>", views.auction, name="auction"),
    path("listings/<int:id_auction>/add-bid", views.new_bid, name="new_bid"),
    path("listings/<int:id_auction>/new-comment", views.new_comment, name="new_comment"),
    path("listings/response-comment/<int:id_comment>", views.response_comment, name="response_comment")
]
