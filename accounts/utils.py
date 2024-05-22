from django.urls import reverse


def create_reset_url(pk, token):
    reset_url = reverse(
            "password_reset",
            kwargs={"pk": pk, "token": token}
        )
    reset_url = f"http://localhost:8000{reset_url}"
    
    return reset_url
