import random
from .models import User
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def send_welcome_email(user: User):
    email_html = f"""
    <html>
        <head>
            <title>Welcome to BlockChain Voting System</title>
        </head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
            }}
            p {{
                margin: 10px 0;
            }}
        </style>
        <body>
          <p> Welcome {user.username}, </p>
            <p>
               We are on a mission to make voting more secure and transparent.
               We are glad to have you on board.   
            </p>
            
            <p>
                <a href="http://localhost:8000/user/{user.first_name}/">
                    Click here to view your profile
                </a>
            </p>

        </body>
    </html>
    """
    mail = EmailMultiAlternatives(
        subject="Welcome to BlockChain Voting System",
        body=email_html,
        from_email=settings.EMAIL_HOST_USER,
        to=[user.email],
    )
    mail.attach_alternative(email_html, "text/html")
    mail.send()


def generate_verification_code():
    return random.randint(100000, 999999)
