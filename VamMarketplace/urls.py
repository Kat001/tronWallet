"""VamMarketplace URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http.response import HttpResponse
from django.urls import path
from django.urls.conf import include

# For Auto-Generating API documentation
from rest_framework.documentation import include_docs_urls


def api_home(request):
    return HttpResponse("Hello World !")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('vod_auth.urls')),
    # path('users/', include('users.urls')),
    path('v1/', include('vod.urls')),
    path('accounts/', include('allauth.urls')),
    # path('v1/school/',include('school.urls')),
    # path('v1/student/',include('student.urls')),
    # path('v1/teacher/',include('teacher.urls')),

    # For Auto-Generating API documentation
    path('api-docs/', include_docs_urls(title='API Documentation')),
    path('', api_home)

]
