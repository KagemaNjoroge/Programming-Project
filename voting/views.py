import datetime
from datetime import timezone
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpRequest
from django.contrib.auth.decorators import login_required

from voting.utils import allocate_votes
from .models import Poll, PollWallet
from blockchain.blockchain import VoteBlockChain, VoteTransaction
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response

vote_blockchain = VoteBlockChain()


@api_view(["POST"])
def vote(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    voter = request.user

    candidate_id = request.data.get("candidate_id")
    votes = int(request.data.get("votes", 1))

    print(f"Voter: {voter.username}, Candidate: {candidate_id}, Votes: {votes}")

    if candidate_id is None:
        return Response({"error": "Candidate ID is required."}, status=400)

    candidate = get_object_or_404(get_user_model(), id=candidate_id)

    # check if the candidate is a participant in the poll
    if candidate not in poll.candidates.all():
        return Response(
            {"error": "Candidate is not a participant in this poll."}, status=400
        )
    # check if the voting has started, or if it has ended
    if poll.start_date > timezone.now():
        return Response({"error": "Voting has not started yet."}, status=400)
    if poll.end_date < timezone.now():
        return Response({"error": "Voting has ended."}, status=400)

    # Get or create PollWallet for voter
    voter_poll_wallet, created = PollWallet.objects.get_or_create(user=voter, poll=poll)

    # Verify if the user has enough votes in the poll wallet
    if voter_poll_wallet.balance < votes:
        return Response(
            {"error": "You do not have enough votes to cast this vote."}, status=403
        )

    # Create VoteTransaction and add to blockchain
    transaction = VoteTransaction(
        sender=voter.username, receiver=candidate.username, votes=votes
    )
    vote_blockchain.create_transaction(transaction)

    # Deduct votes from voter balance
    initial_voter_balance = voter_poll_wallet.balance
    voter_poll_wallet.balance -= votes
    voter_poll_wallet.save()
    print(
        f"Voter {voter.username} balance before: {initial_voter_balance}, after: {voter_poll_wallet.balance}"
    )

    # Update candidate's balance in their PollWallet
    candidate_wallet, created = PollWallet.objects.get_or_create(
        user=candidate, poll=poll
    )
    initial_candidate_balance = candidate_wallet.balance
    candidate_wallet.balance += votes
    candidate_wallet.save()
    print(
        f"Candidate {candidate.username} balance before: {initial_candidate_balance}, after: {candidate_wallet.balance}"
    )

    return Response({"message": "Vote cast successfully."})


@swagger_auto_schema(
    method="get",
    operation_description="Mine pending transactions",
)
@login_required(login_url="/accounts/login/")
@api_view(["GET"])
def mine_transactions(request):
    vote_blockchain.mine_pending_transactions()
    return JsonResponse({"message": "Pending transactions mined."})


@swagger_auto_schema(
    method="post",
    operation_description="Allocate votes to users in a poll",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "votes_{user_id}": openapi.Schema(
                type=openapi.TYPE_INTEGER, description="Number of votes for user"
            )
        },
    ),
)
@api_view(["POST"])
def allocate_votes_view(request, poll_id):
    allocations = {}
    for key, value in request.data.items():
        if key.startswith("votes_"):
            user_id = int(key.split("_")[1])
            votes = int(value)
            allocations[user_id] = votes

    allocate_votes(poll_id, allocations)
    return Response(
        {
            "message": "Votes allocated successfully.",
            "allocations": allocations,
            "poll_id": poll_id,
            "poll_title": Poll.objects.get(id=poll_id).title,
        }
    )


@login_required(login_url="/accounts/login/")
def voting_template_view(request: HttpRequest):
    # wallets
    wallet = PollWallet.objects.filter(user=request.user).order_by("-poll__start_date").filter(
        poll__end_date__gte=datetime.datetime.now(),
        poll__start_date__lte=datetime.datetime.now(),
    )

    return render(request, "voting/voting.html", {"wallet": wallet})


@login_required(login_url="/accounts/login/")
def home(request: HttpRequest):
    return render(request, "system/index.html")
