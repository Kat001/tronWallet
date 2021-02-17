from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import update_session_auth_hash
from django.core.files.storage import FileSystemStorage

from account.models import Account
import datetime
from datetime import date

from django.db.models import Sum


# Create your views here.


def change_password(request):
    user = request.user
    user_pass = user.password

    if request.method == 'POST':
        o_pass = request.POST.get('o_pass')
        n_pass = request.POST.get('n_pass')
        c_pass = request.POST.get('c_pass')

        cheak = user.check_password(o_pass)

        if cheak:
            if n_pass == c_pass:
                p = make_password(n_pass)
                obj = Account.objects.get(username=user.username)
                user.set_password(n_pass)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Password Changed successfully!!")
                return redirect('change_password')
            else:
                messages.error(
                    request, 'New password and confirm password should be same!!')
                return redirect('change_password')
        else:
            messages.error(request, "Old Password is Wrong!!")
            return redirect('change_password')

    return render(request, 'change_password.html')
