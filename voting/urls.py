from django.urls import path
from .views import vote, mine_transactions, allocate_votes_view, voting_template_view, home
app_name = "voting"
urlpatterns = [
    path("vote/<int:poll_id>/", vote, name="vote"),
    path("mine/", mine_transactions, name="mine_transactions"),
    path("allocate/<int:poll_id>/", allocate_votes_view, name="allocate_votes"),
    path("", home, name="home"),
]
