from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from .permissions import IsOwnerOrReadOnly
from .models import Video, Comment, Like, Subscriber,Favorite,Rating
from .serializers import (
    VideoSerializer,
    CommentSerializer,
    LikeSerializer,
    SubscriberSerializer,
    RatingSerializer,
    FavoriteSerializer
)


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


@api_view(["POST"])
def toggle_like(request, id):
    user = request.user
    if not user.is_authenticated:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    video = get_object_or_404(Video, id=id)
    if Like.objects.filter(user=user, video=video).exists():
        Like.objects.filter(user=user, video=video).delete()
    else:
        Like.objects.create(user=user, video=video)
    return Response(status=status.HTTP_201_CREATED)


@api_view(["POST"])
def toggle_subscribe(request, id):
    user = request.user
    if not user.is_authenticated:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    if Subscriber.objects.filter(user=user, subscribed_to=id).exists():
        Subscriber.objects.filter(user=user, subscribed_to=id).delete()
    else:
        Subscriber.objects.create(user=user, subscribed_to=id)
    return Response(status=status.HTTP_201_CREATED)

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer  

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [IsAuthenticated]  # Доступ только зарегистрированным пользователям
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsOwnerOrReadOnly]  # Доступ только владельцам избранных товаров
        return [permission() for permission in self.permission_classes]
