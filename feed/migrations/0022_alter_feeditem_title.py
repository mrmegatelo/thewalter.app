# Generated by Django 5.1.3 on 2024-11-11 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0021_alter_feed_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feeditem',
            name='title',
            field=models.CharField(max_length=400),
        ),
    ]
