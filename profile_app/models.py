from django.db import models
from account.models import Account


class Requested_Fund(models.Model):
    user_name = models.CharField(max_length=20)
    date = models.DateField(default='1999-01-01')
    fund = models.FloatField(default=0)
    transection_no = models.FloatField(default=0)
    proof = models.ImageField(default="default.jpg", upload_to="profile_pics")
    status = models.CharField(max_length=10, default="Pending")

    def __str__(self):
        return(f'{self.user_name}')


class Fund(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    available_fund = models.FloatField(default=0)

    @property
    def username(self):
        return self.user

    def __str__(self):
        return(f'{self.user}')


class All_Direct_Income(models.Model):
    #user 	= models.ForeignKey(Account, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=60, default="")
    activated_id = models.CharField(max_length=60, default="")
    date = models.DateField(auto_now_add=True)
    amount = models.FloatField(default=0)

    def __str__(self):
        return(f'{self.user_name}')


class All_Roi_Income(models.Model):
    #user 	= models.ForeignKey(Account, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=60, default="")
    date = models.DateField(auto_now_add=True)
    amount = models.FloatField(default=0)


class Update_Roi_Income(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    #user = models.CharField(max_length=60,default="")
    date = models.DateField(auto_now_add=True)
    amount = models.FloatField(default=0)
    days = models.PositiveIntegerField(default=0)

    def __str__(self):
        return(f'{self.user}')

    @property
    def username(self):
        return self.user


class All_Level_Income(models.Model):
    #user 	= models.ForeignKey(Account, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=60, default="")
    activated_id = models.CharField(max_length=60, default="")
    date = models.DateField(auto_now_add=True)
    level = models.CharField(max_length=10, default="")
    amount = models.FloatField(default=0)

    def __str__(self):
        return(f'{self.user_name}')


class Fund_History(models.Model):
    user_name = models.CharField(max_length=60, default="")
    activated_id = models.CharField(max_length=60, default="")
    date = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField(default=0)

    def __str__(self):
        return(f'{self.user_name}')


'''class Bank_Info(models.Model):
	user = models.OneToOneField(Account, on_delete=models.CASCADE)
	account_holder_name = models.CharField(max_length=40, default="-")
	account_number = models.CharField(max_length=30, default='-')
	branch_name = models.CharField(max_length=40, default='-')
	ifsc_code = models.CharField(max_length=20, default="-")
	bank_name = models.CharField(max_length=30, default='-')
	nominee_name = models.CharField(max_length=30, default="-")
	aadhar_number = models.CharField(max_length=12, default="-")
	pan_number = models.CharField(max_length=10, default="-")
	aadhar_image = models.ImageField(
		default="default.jpg", upload_to="adhar_pics", null=True, blank=True)
	pan_image = models.ImageField(
		default="default.jpg", upload_to="pan_pics", null=True, blank=True)
	p_image = models.ImageField(default="default.jpg", upload_to="profile_pics")
	cheak = models.BooleanField(default=False)

	@property
	def username(self):
		return self.user.username

	def __str__(self):
		return(f'{self.user.username}')'''
