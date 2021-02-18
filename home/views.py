from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from account.models import Account
from django.contrib.auth import logout
from django.contrib.auth.models import auth

import random


# Create your views here.


def index(request):
    d = {

    }
    return render(request, 'index.html', d)


def register(request):
    if request.user.is_authenticated:
        logout(request)
    if request.method == 'POST':
        name = request.POST.get('name')
        sponser = request.POST.get('sponser')
        mobile_no = request.POST.get('mobile')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        print(pass1, pass2)

        pass12 = make_password(pass1)

        if pass1 != pass2:

            try:
                spn_obj = Account.objects.get(username=sponser)
                c = Account.objects.all().count()
                k = c + 2

                while True:
                    rand_num = random.randint(500000, 599999)
                    u_name = 'FI' + str(rand_num)
                    if Account.objects.filter(username=u_name).exists():
                        pass
                    else:
                        break

                user = Account(username=u_name, sponser=sponser, password=pass12, first_name=name,
                               email=email, txn_password=pass2, phon_no=mobile_no, rem_paas=pass1)

                user.save()

                request.session['user_name'] = u_name
                request.session['spn'] = sponser
                request.session['u_pass'] = pass1
                request.session['txn_pass'] = pass2
                request.session['name'] = name

                user = auth.authenticate(username=u_name, password=pass1)
                if user is not None:
                    auth.login(request, user)

                messages.success(request, 'Update Profile First!!')
                return redirect('detail')

            except Exception as e:
                print(e)
                messages.error(request, "Sponser Does Not Exist!!")
                return redirect('register')
        else:
            messages.error(
                request, 'Password and transection password can not be same!!')
            return redirect('register')

    else:
        pass

    d = {}
    return render(request, 'register.html', d)


def login1(request):
    d = {}
    return render(request, 'login1.html', d)
