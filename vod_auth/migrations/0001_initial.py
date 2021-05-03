# Generated by Django 3.1.7 on 2021-04-16 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('role', models.CharField(choices=[('SUPER_ADMIN', 'SUPER_ADMIN'), ('TEACHER', 'TEACHER'), ('STUDENT', 'STUDENT')], default='STUDENT', max_length=15)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=100, null=True)),
                ('phone', models.CharField(max_length=15, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=255, null=True)),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('date_of_birth', models.DateField(null=True)),
                ('gender', models.CharField(choices=[('male', 'MALE'), ('female', 'FEMALE')], default='', max_length=10)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]