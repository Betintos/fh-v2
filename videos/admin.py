from django.contrib import admin

from .models import Video, Comment, Like, Subscriber

# Register your models here.
admin.site.register(Video)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Subscriber)
