# Generated by Django 5.1.2 on 2024-11-05 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0019_alter_attachment_type_alter_servicefeed_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='feed',
            options={'ordering': ['title']},
        ),
        migrations.AlterField(
            model_name='feed',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]