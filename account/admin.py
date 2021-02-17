from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Account

#from django.contrib.auth.admin import UserAdmin
#from profile_app.models import *

from django.utils.html import format_html
from django.urls import reverse
# from django.urls import url
from django.conf.urls import include, url
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse

from django.urls import reverse
from django.utils.http import urlencode

from django.contrib.auth.models import Group


# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('username', 'email', 'sponser',
                    'is_active1', 'date_active')
    search_fields = ('email', 'username',)
    readonly_fields = ('sponser', 'username', 'downline', 'upline')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    actions = ['assign_ranks']


'''class All_Withrawal_Request1_Admin(admin.ModelAdmin):
    list_display = ('username', 'date', 'account_holder_name', 'account_number', 'ifsc_code', 'branch_name', 'amount', 'Rupya',
                    'accept_withrawal', 'cancel_withrawal',)
    search_fields = ('username',)
    list_filter = ()
    fieldsets = ()


class All_Withrawal_Admin(admin.ModelAdmin):
    list_display = ('username', 'date', 'account_holder_name',
                    'account_number', 'ifsc_code', 'branch_name', 'amount', 'status',)
    search_fields = ('username',)
    list_filter = ()
    fieldsets = ()

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False'''


admin.site.unregister(Group)
admin.site.register(Account, AccountAdmin)
