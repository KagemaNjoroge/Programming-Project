from django.urls import path

from .views import (

    mine_transactions,
    allocate_votes_view,
    home,
    create_new_poll_page,
    PollListView,
    my_polls_template_view,
    poll_invites_template_view,
    PollInvitationsView,
    invite_users_for_poll,
    voting_template_view,
)

app_name = "voting"
urlpatterns = [

    path("mine/", mine_transactions, name="mine_transactions"),
    path("allocate/<int:poll_id>/", allocate_votes_view, name="allocate_votes"),
    path("", home, name="home"),
    path("create/", create_new_poll_page, name="create_new_poll"),
    path("polls/", PollListView.as_view(), name="polls"),
    path("my-polls/", my_polls_template_view, name="my_polls"),
    path("poll-invites/", poll_invites_template_view, name="poll_invites"),
    path("poll-invitations/", PollInvitationsView.as_view(), name="poll_invitations"),
    path(
        "poll-invitations/<int:id>/",
        PollInvitationsView.as_view(),
        name="poll_invitations",
    ),
    path("invite/<int:poll_id>/", invite_users_for_poll, name="invite_users_for_poll"),
    path("voting/<int:poll_id>/", voting_template_view, name="voting"),
]
