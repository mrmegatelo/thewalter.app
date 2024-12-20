# Generated by Django 5.1.3 on 2024-11-11 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0022_alter_feeditem_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='feeditem',
            name='preview',
            field=models.URLField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='feeditem',
            name='link',
            field=models.URLField(blank=True, max_length=500, unique=True),
        ),
    ]
