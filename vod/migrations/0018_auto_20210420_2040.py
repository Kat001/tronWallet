# Generated by Django 3.1.7 on 2021-04-20 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vod', '0017_courseenrollment_is_enabled'),
    ]

    operations = [
        migrations.AddField(
            model_name='modulevideo',
            name='subtitle',
            field=models.CharField(default='', help_text='Subtitle of the video', max_length=50),
        ),
        migrations.AlterField(
            model_name='modulevideo',
            name='title',
            field=models.CharField(help_text='Name of the video', max_length=50),
        ),
    ]
