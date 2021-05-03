from django.db import models
from django.db.models.fields import related
from vod_auth.models import User


class ObjectDoesNotExistManager(models.Manager):
    def get(self, *args, **kwargs):
        qs = self.get_queryset().filter(*args, **kwargs)
        if qs.count() == 1:
            return qs.first()
        return None


class Instructor(models.Model):
    account = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True)

    objects = ObjectDoesNotExistManager()

    def __str__(self):
        return str(self.account)


class Course(models.Model):
    name = models.CharField(
        max_length=50, help_text="Name of the course")
    slug = models.CharField(max_length=100, default='course-slug',
                            help_text="Slug name of the course for human friendly urls")
    instructor = models.ForeignKey(
        Instructor, on_delete=models.CASCADE, related_name='courses')

    course_image = models.CharField(max_length=1024, default="")
    display_order = models.IntegerField(default=0)  # 0 means don't display
    short_description = models.CharField(
        max_length=50, help_text="One liner description for course", default="")
    description = models.CharField(
        max_length=1000, help_text="Course description", default="")
    default_price = models.IntegerField(
        default=1000,
        help_text="Course default price for display")
    discounted_price = models.IntegerField(
        default=500,
        help_text="Course default discounted rate")
    discount_rate = models.IntegerField(
        default=50,
        help_text="Course default discount rate")

    objects = ObjectDoesNotExistManager()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'VOD_Course'


class Student(models.Model):
    account = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='vod_student')

    objects = ObjectDoesNotExistManager()

    def __str__(self):
        return str(self.account)

    class Meta:
        db_table = 'VOD_Student'


class CourseModule(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='modules')
    name = models.CharField(
        max_length=50, help_text="Name of the course module")

    def __str__(self):
        return self.name


class CourseTestimonial(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='testimonials')
    name = models.CharField(
        max_length=64, help_text="Name of the user giving testimonial")
    profile_pic = models.CharField(
        max_length=128, help_text="Profile picture of user giving testimonial")
    description = models.CharField(
        max_length=256, help_text="Description of the testimonial")


class CourseFAQ(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(
        max_length=64, help_text="FAQ Question")
    answer = models.CharField(
        max_length=256, help_text="FAQ Answer")


class ModuleVideo(models.Model):
    module = models.ForeignKey(
        CourseModule, on_delete=models.CASCADE, related_name='video')
    title = models.CharField(
        max_length=50, help_text="Name of the video")
    subtitle = models.CharField(
        max_length=50, help_text="Subtitle of the video", default="")
    description = models.CharField(
        max_length=250, help_text="Description of the video")
    thumbnail = models.CharField(
        max_length=256, default="", help_text="Thumbnail URL for the video")
    public_url = models.CharField(
        max_length=300, help_text="Stream URL of the demo video")
    private_url = models.CharField(
        max_length=300, help_text="Stream URL of the full video")
    dishabled = models.BooleanField(default=False)

    video_highlight_order = models.IntegerField(
        default=0)  # 0 represents don't show in highlights

    objects = ObjectDoesNotExistManager()

    def __str__(self):
        return self.module


class MuxAsset(models.Model):
    video = models.ForeignKey(
        ModuleVideo, on_delete=models.CASCADE, related_name='mux_assets')
    asset_id = models.CharField(max_length=128)
    playback_id = models.CharField(max_length=128, default='')
    # "COMPLETE", "PROCESSING", "ERROR"
    # choices will be made as a list after we have decided all the possible values.
    status = models.CharField(max_length=16)


class CourseEnrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_enabled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student} :: {self.course.name}"


class EnrollmentTransaction(models.Model):
    enrollment = models.ForeignKey(
        CourseEnrollment, on_delete=models.CASCADE, related_name='transactions')
    razorpay_order_id = models.CharField(max_length=200, null=True)
    razorpay_payment_id = models.CharField(
        max_length=200, null=True)
    razorpay_signature = models.CharField(
        max_length=200, null=True)
    is_verified = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
