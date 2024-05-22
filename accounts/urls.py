from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import SimpleRouter
from django.urls import path

from .views import RegisterView, ActivationView, AccountViewSet, AccountDetailView


router = SimpleRouter()

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path(
        "activate/<str:email>/<str:activation_code>/",
        ActivationView.as_view(),
        name="activate",
    ),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", AccountViewSet.as_view({"get": "list"})),
    path("<int:pk>/", AccountViewSet.as_view({"put": "update", "delete": "destroy", "patch": "partial_update", "get": "retrieve"})),
    path("<str:email>/", AccountDetailView.as_view())
]
