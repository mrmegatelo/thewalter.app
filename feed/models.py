from django.db import models


# Create your models here.
class Feed(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    link = models.URLField()
    pub_date = models.DateTimeField()
    guid = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.title


class FeedItem(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    link = models.URLField()
    pub_date = models.DateTimeField()
    guid = models.CharField(max_length=200, unique=True)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
