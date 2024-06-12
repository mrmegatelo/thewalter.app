from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


# Create your models here.
class Feed(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    url = models.URLField()
    rss_url = models.URLField()
    pub_date = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.pub_date = datetime.now()
        # Create a slug if it is not provided. Just to make it easier for the user.
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class FeedItem(models.Model):
    title = models.CharField(max_length=200)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    description = models.TextField()
    link = models.URLField()
    pub_date = models.DateTimeField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-pub_date']
