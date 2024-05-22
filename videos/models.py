from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='videos/')
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos')

    def __str__(self):
        return self.title


class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Subscriber(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="subscription"
    )
    subscribed_to = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="subscribers"
    )
    subscribed_at = models.DateTimeField(auto_now_add=True)


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Video, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Video, on_delete=models.CASCADE)
    created_at= models.DateTimeField(auto_now_add=True)