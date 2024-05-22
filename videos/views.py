from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Video, Comment, Like, Subscriber
from .serializers import (
    VideoSerializer,
    CommentSerializer,
    LikeSerializer,
    SubscriberSerializer,
)
from .permissions import IsOwnerOrReadonlyComment, IsOwnerOrReadonlyVideo


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            self.permission_classes = [AllowAny]
        elif self.action in ["create"]:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes = [IsOwnerOrReadonlyVideo]
        return [permission() for permission in self.permission_classes]

    def get_serializer_context(self):
        return {"request": self.request}


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            self.permission_classes = [AllowAny]
        elif self.action in ["create"]:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes = [IsOwnerOrReadonlyComment]
        return [permission() for permission in self.permission_classes]

    def get_serializer_context(self):
        return {"request": self.request}


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
