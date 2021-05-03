import json
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from django.http.response import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework.views import APIView

from dj_rest_auth.views import UserDetailsView, LoginView, LogoutView

from dj_rest_auth.registration.views import RegisterView


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter


class UserLogin(LoginView):
    pass

class UserLogout(LogoutView):
    pass

class RegisterUser(RegisterView):
    def create(self, request, *args, **kwargs):
        print(request.data)
        return super().create(request, *args, **kwargs)

class UserInfo(UserDetailsView):
    def get_object(self):
        try:
            user = self.request.user
        except:
            user = "Anonymous"

        print("User ", user)
        return user
