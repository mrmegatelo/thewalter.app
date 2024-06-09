from django.db import models


# Create your models here.
class Feed(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True)
    guid = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    url = models.URLField()
    rss_url = models.URLField()
    pub_date = models.DateTimeField()

    def __str__(self):
        return self.title


class FeedItem(models.Model):
    title = models.CharField(max_length=200)
    guid = models.CharField(max_length=200, unique=True)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    description = models.TextField()
    link = models.URLField()
    pub_date = models.DateTimeField()

    def __str__(self):
        return self.title
