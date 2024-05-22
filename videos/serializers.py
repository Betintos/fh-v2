from rest_framework import serializers

from .models import Video, Comment, Like, Subscriber, Favorite, Rating


class VideoSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    class Meta:
        model = Video
        fields = "__all__"

    def get_likes_count(self, obj):
        return obj.likes.count()

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        video = super().create(validated_data)
        video.save()
        return video


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        comment = super().create(validated_data)
        comment.save()
        return comment

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"


class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = "__all__"

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Favorite
        exclude=['user']
