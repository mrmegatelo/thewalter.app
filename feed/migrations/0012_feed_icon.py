# Generated by Django 5.0.6 on 2024-07-10 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0011_remove_feed_created_by_feed_subscribers'),
    ]

    operations = [
        migrations.AddField(
            model_name='feed',
            name='icon',
            field=models.URLField(blank=True),
        ),
    ]