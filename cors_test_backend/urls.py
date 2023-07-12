"""
URL configuration for cors_test_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path #, include

from cookies import views as cookie_views
from registration import views as reg_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("sample/", cookie_views.MyView.as_view(), name="sample"),
    path("get_user/", reg_views.GetUser.as_view(), name="get_user"),
    path("get_csrf/", cookie_views.GetCSRFToken.as_view(), name="get_csrf"),
    # path("accounts/", include("django.contrib.auth.urls")),
    path("my_login/", reg_views.MyLoginView.as_view(), name="my_login"),
    path("my_logout/", reg_views.MyLogoutView.as_view(), name="my_logout"),
    path("register/", reg_views.RegisterUser.as_view(), name="register"),
]
