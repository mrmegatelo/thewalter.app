# Generated by Django 5.0.6 on 2024-07-11 19:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0013_alter_feed_icon'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, choices=[('audio', 'Audio')], max_length=20)),
                ('url', models.URLField()),
                ('feed_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='feed.feeditem')),
            ],
        ),
    ]
