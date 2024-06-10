from .models import Poll, PollWallet
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.contrib.auth.models import AbstractBaseUser
from django.core.mail import EmailMessage


def allocate_votes(poll_id, allocations):
    # Example usage:
    # poll_id = 1  # Poll ID
    # allocations = {
    #     1: 10,  # User ID 1 gets 10 votes
    #     2: 5,   # User ID 2 gets 5 votes
    # }
    poll = Poll.objects.get(id=poll_id)
    for user_id, votes in allocations.items():
        user = get_user_model().objects.get(id=user_id)
        poll_wallet, created = PollWallet.objects.get_or_create(user=user, poll=poll)
        poll_wallet.balance += votes
        poll_wallet.save()


def send_voting_invitation(poll: Poll, user: AbstractBaseUser):
    html_content = "voting/voting_invite_email.html"
    subject = f"Invitation to vote in {poll.title}"
    username = user.get_username()
    voting_link = "https://tomorrow.co.ke"

    email = EmailMessage(
        subject,
        render_to_string(
            html_content,
            {
                "username": username,
                "voting_link": voting_link,
                "poll_name": poll.title,
                "poll_description": poll.description,
            },
        ),
        to=[user.email],
    )
    email.content_subtype = "html"
    email.send()
