# Generated by Django 5.1.4 on 2024-12-16 09:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0030_alter_servicefeed_type_feeditemaction'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ServiceFeed',
        ),
    ]
