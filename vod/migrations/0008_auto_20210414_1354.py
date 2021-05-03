# Generated by Django 3.1.7 on 2021-04-14 08:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vod', '0007_remove_student_enrolled_courses'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='default_price',
            field=models.IntegerField(default=1000, help_text='Course default price for display'),
        ),
        migrations.AddField(
            model_name='course',
            name='discount_rate',
            field=models.IntegerField(default=50, help_text='Course default discount rate'),
        ),
        migrations.AddField(
            model_name='course',
            name='discounted_price',
            field=models.IntegerField(default=500, help_text='Course default discounted rate'),
        ),
        migrations.AddField(
            model_name='course',
            name='slug',
            field=models.CharField(default='course-slug', help_text='Slug name of the course for human friendly urls', max_length=100),
        ),
        migrations.AddField(
            model_name='modulevideo',
            name='course_highlight_order',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='CourseTestimonial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the user giving testimonial', max_length=64)),
                ('profile_pic', models.CharField(help_text='Profile picture of user giving testimonial', max_length=128)),
                ('description', models.CharField(help_text='Description of the testimonial', max_length=256)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='testimonials', to='vod.course')),
            ],
        ),
        migrations.CreateModel(
            name='CourseFAQ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(help_text='FAQ Question', max_length=64)),
                ('answer', models.CharField(help_text='FAQ Answer', max_length=256)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='faqs', to='vod.course')),
            ],
        ),
    ]