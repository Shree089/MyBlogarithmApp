from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import reverse

class Post(models.Model):
    title = models.CharField(max_length=25)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete= models.CASCADE, related_name='author')
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    comments = models.ManyToManyField(User, blank=True, related_name='comments')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail',kwargs={'pk':self.pk})

    def total_likes(self):
        return self.likes.count()