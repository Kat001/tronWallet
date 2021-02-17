
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email", max_length=60, unique=False, blank=True, null=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(
        verbose_name='date joined', auto_now_add=True)
    date_active = models.DateTimeField(
        verbose_name='date active', default='2000-01-01 06:00')
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_active1 = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    down_team = models.IntegerField(default=0, blank=True, null=True)
    total_team = models.TextField(max_length=10000000, blank=True, null=True)
    total_rank_income = models.FloatField(default=0)
    total_level_income = models.FloatField(default=0)
    total_roi_income = models.FloatField(default=0)
    total_direct_income = models.FloatField(default=0)
    activation_amount = models.FloatField(default=0)
    refund = models.FloatField(default=0)
    first_name = models.CharField(
        max_length=30, unique=False, blank=True, null=True)
    last_name = models.CharField(
        max_length=30, unique=False, blank=True, null=True)
    sponser = models.CharField(
        max_length=30, unique=False, blank=True, null=True)
    upline = models.CharField(
        max_length=30, unique=False, blank=True, null=True)
    downline = models.CharField(
        max_length=30, unique=False, blank=True, null=True)
    txn_password = models.CharField(max_length=30, null=False)
    phon_no = models.CharField(max_length=12, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    dob = models.DateTimeField(
        verbose_name='date of birth', null=True, blank=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    zip = models.CharField(max_length=6, blank=True, null=True)
    image = models.ImageField(
        default="default.jpg", upload_to="profile_pics", null=True, blank=True)
    rem_paas = models.CharField(max_length=30, null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = MyAccountManager()

    def __str__(self):
        return self.username

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True


'''class All_Withrawal_Request1(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    account_holder_name = models.CharField(max_length=40, default="")
    account_number = models.CharField(max_length=30, default='')
    branch_name = models.CharField(max_length=40, default='')
    ifsc_code = models.CharField(max_length=20, default="")
    bank_name = models.CharField(max_length=30, default='')
    status = models.CharField(max_length=30, default="")
    amount = models.FloatField(default=0)
    charge = models.FloatField(default=0)
    w_amount = models.FloatField(default=0)

    @property
    def username(self):
        return self.user.username

    def __str__(self):
        return(f'{self.user.username}')


class All_Withrawal(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    account_holder_name = models.CharField(max_length=40, default="")
    account_number = models.CharField(max_length=30, default='')
    branch_name = models.CharField(max_length=40, default='')
    ifsc_code = models.CharField(max_length=20, default="")
    bank_name = models.CharField(max_length=30, default='')
    status = models.CharField(max_length=30, default="")
    amount = models.FloatField(default=0)
    charge = models.FloatField(default=0)
    w_amount = models.FloatField(default=0)

    @property
    def username(self):
        return self.user.username

    def __str__(self):
        return(f'{self.user.username}')

'''
