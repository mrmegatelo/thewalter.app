# Generated by Django 5.0.6 on 2024-07-12 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0014_attachment'),
    ]

    operations = [
        migrations.AddField(
            model_name='feeditem',
            name='has_paid_content',
            field=models.BooleanField(default=False),
        ),
    ]