from datetime import datetime
from urllib.parse import urlparse

from django.contrib.auth import get_user_model
from django.db import models
from slugify import slugify


# Create your models here.
class Feed(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    url = models.URLField(unique=True)
    rss_url = models.URLField(unique=True)
    icon = models.URLField(max_length=500, blank=True)
    pub_date = models.DateTimeField()
    subscribers = models.ManyToManyField(get_user_model(), blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.pub_date = datetime.now()
        # Create a slug if it is not provided. Just to make it easier for the user.
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def domain_name(self):
        return urlparse(self.url).netloc

    class Meta:
        ordering = ["title"]


class FeedItem(models.Model):
    title = models.CharField(max_length=400)
    feed = models.ForeignKey(Feed, related_name="feed_items", on_delete=models.CASCADE)
    description = models.TextField()
    link = models.URLField(max_length=500, unique=True, blank=True)
    pub_date = models.DateTimeField()
    preview = models.URLField(max_length=500, blank=True, null=True)
    has_paid_content = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    @property
    def pub_day(self):
        """
        Return the publication date without the time. This could be a perfomance issue if the database is large.
        :return:
        """
        return self.pub_date.replace(hour=0, minute=0, second=0, microsecond=0)

    @property
    def type(self):
        """
        Return the type of the feed item based on the type of its attachments.
        If there are no attachments, return an `article` type.
        :return:
        """
        first_attachment = self.attachments.first()
        if first_attachment:
            match first_attachment.type:
                case Attachment.Type.AUDIO:
                    return "audio"
                case Attachment.Type.VIDEO | Attachment.Type.EMBED:
                    return "video"
        return "article"

    class Meta:
        ordering = ["-pub_date"]


class Collection(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    feeds = models.ManyToManyField(Feed, blank=True)

    def save(self, *args, **kwargs):
        self.pub_date = datetime.now()
        # Create a slug if it is not provided. Just to make it easier for the user.
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'title'],
                name='unique_name_per_user',
            )
        ]


class ServiceFeed(models.Model):
    class Type(models.TextChoices):
        LIKED = "liked"
        DISLIKED = "disliked"
        VIEWED = "viewed"

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=Type, default=Type.LIKED)
    feed_items = models.ManyToManyField(
        FeedItem, related_name="service_feeds", blank=True
    )

    def __str__(self):
        return f"{self.type} feed items for {self.user}"


class Attachment(models.Model):
    class Type(models.TextChoices):
        AUDIO = "audio"
        VIDEO = "video"
        EMBED = "embed"

    feed_item = models.ForeignKey(
        FeedItem, related_name="attachments", on_delete=models.CASCADE
    )
    type = models.CharField(max_length=20, choices=Type.choices, blank=True)
    url = models.URLField()


class UserSettings(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    hidden_feed_items = models.ManyToManyField(
        FeedItem, blank=True, related_name="hidden"
    )
    liked_feed_items = models.ManyToManyField(
        FeedItem, blank=True, related_name="liked"
    )


class Invite(models.Model):
    class Status(models.TextChoices):
        PENDING = "Pending"
        SENT = "Sent"
        ACCEPTED = "Accepted"
        ACTIVATED = "Activated"

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    accepted_at = models.DateTimeField(null=True, blank=True)
    activated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        match self.status:
            case Invite.Status.PENDING:
                return f"{self.status} at {self.created_at}"
            case Invite.Status.SENT:
                return f"{self.status} at {self.sent_at}"
            case Invite.Status.ACCEPTED:
                return f"{self.status} at {self.accepted_at}"
            case Invite.Status.ACTIVATED:
                return f"{self.status} at {self.activated_at}"


class WaitlistRequest(models.Model):
    email = models.EmailField()
    user = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    invite = models.OneToOneField(
        "Invite", on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.email
