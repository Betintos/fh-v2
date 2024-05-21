from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VideoViewSet, CommentViewSet, FavoriteViewSet,RatingViewSet,toggle_like, toggle_subscribe

router = DefaultRouter()
router.register(r"videos", VideoViewSet)
router.register(r"comments", CommentViewSet)
router.register(r'rating', RatingViewSet)
router.register(r'favorite', FavoriteViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("like/<int:id>/", toggle_like),
    path("subscribe/<int:id>/", toggle_subscribe),
]