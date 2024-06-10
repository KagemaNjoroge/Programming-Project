from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now


class User(AbstractUser):
    ROLE_CHOICES = [
        ("voter", "Voter"),
        ("candidate", "Candidate"),
        ("admin", "Admin"),
        ("election_officer", "Election Officer"),  # Additional role
        ("auditor", "Auditor"),  # Additional role
    ]

    email_verified = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    phone_verified = models.BooleanField(default=False)
    # profile image
    profile_image = models.ImageField(
        upload_to="profile_images/", default="profile/default/avatar.png"
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="voter")

    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username


class VerificationCodes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    expires_at = models.DateTimeField(default=now() + timedelta(minutes=5))

    def __str__(self):
        return f"{self.user.username} - {self.code}"

    class Meta:
        verbose_name_plural = "Verification Codes"
