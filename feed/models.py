from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from slugify import slugify


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

    @property
    def pub_day(self):
        """
        Return the publication date without the time. This could be a perfomance issue if the database is large.
        :return:
        """
        return self.pub_date.replace(hour=0, minute=0, second=0, microsecond=0)

    class Meta:
        ordering = ['-pub_date']


class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hidden_feed_items = models.ManyToManyField(FeedItem, blank=True)


class WaitlistRequest(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email
