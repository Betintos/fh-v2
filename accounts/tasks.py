from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from celery import shared_task


@shared_task
def send_activation_code(email, activation_code):
    context = {
        "text_detail": "Спасибо за регистрацию",
        "email": email,
        "domain": "http://localhost:8000",
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


@shared_task
def send_password_reset_link(email, link):
    context = {
        "email": email,
        "link": link,
    }
    msg_html = render_to_string("password_reset.html", context)
    message = strip_tags(msg_html)
    send_mail(
        "Password reset",
        message,
        "admin@admin.com",
        [email],
        html_message=msg_html,
        fail_silently=False,
    )