from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Video, Comment, Like, Subscriber
from .serializers import (
    VideoSerializer,
    CommentSerializer,
    LikeSerializer,
    SubscriberSerializer,
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
