import os

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from celery import shared_task


@shared_task
def send_activation_code(email, activation_code):
    domain = os.getenv("DOMAIN", "http://localhost:8000")
    context = {
        "text_detail": "Спасибо за регистрацию",
        "email": email,
        "domain": domain,
        "activation_code": activation_code,
    }
    msg_html = render_to_string("activation_email.html", context)
    message = strip_tags(msg_html)
    send_mail(
        "Account activation",
        message,
        "admin@gmail.com",
        [email],
        html_message=msg_html,
        fail_silently=False,
    )
