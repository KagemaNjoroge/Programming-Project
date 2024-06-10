from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now


class Poll(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=now)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    candidates = models.ManyToManyField(get_user_model(), related_name="candidates", blank=True)
    avatar = models.ImageField(upload_to="polls/", null=True, blank=True, default="polls/default.jpg")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Polls"
        verbose_name = "Poll"


class PollWallet(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)

    def __str__(self):
        return f'Wallet: {self.id}'

    class Meta:
        verbose_name_plural = "Poll Wallets"
        verbose_name = "Poll Wallet"
