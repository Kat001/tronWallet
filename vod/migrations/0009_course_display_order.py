# Generated by Django 3.1.7 on 2021-04-14 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vod', '0008_auto_20210414_1354'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='display_order',
            field=models.IntegerField(default=0),
        ),
    ]
