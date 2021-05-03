from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, UserManager


class UserManager(BaseUserManager):

    def get_or_none(self, *args, **kwargs):
        qs = self.get_queryset().filter(*args, **kwargs)
        if qs.count() == 1:
            return qs.first()
        return None

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a Superuser with the given email and password.
        """

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff = True")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser = True")
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    ROLE_TYPES = (
        ('SUPER_ADMIN', 'SUPER_ADMIN'),
        ('TEACHER', 'TEACHER'),
        ('STUDENT', 'STUDENT')
    )
    role = models.CharField(
        max_length=15, choices=ROLE_TYPES, default='STUDENT')
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=100, null=True)
    phone = models.CharField(unique=False, max_length=15)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(
        choices=(("male", "MALE"), ("female", "FEMALE")), default="", max_length=10)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        print('model method', self.first_name)
        return f'{self.first_name} {self.last_name}'

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True
