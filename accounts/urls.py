from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import SimpleRouter

from .views import RegisterView, ActivationView, AccountViewSet, AccountDetailView


router = SimpleRouter()
router.register(r"", AccountViewSet)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path(
        "activate/<str:email>/<str:activation_code>/",
        ActivationView.as_view(),
        name="activate",
    ),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", include(router.urls)),
    path("<str:email>", AccountDetailView.as_view())
]
