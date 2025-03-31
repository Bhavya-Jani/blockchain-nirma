"""
URL configuration for blockchain project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from blockchain import views
from .api_views import get_wallets

urlpatterns = [
    path('admin/', admin.site.urls),  # Default Admin Panel
    path('',views.homepage,name='Home'),
    path('try/',views.tryhtml,name='try'),
    path('login/', views.login_view, name='login'),
    path('sign_up/',views.signin,name="signup"),
    path('status/', views.blockchain_status, name='blockchain_status'),
    path("solana-status/", views.solana_status_view, name="solana_status"),
    path("solana-latest-block/", views.solana_latest_block_view, name="solana_latest_block"),
    path("about_us/",views.aboutus,name="aboutus"),
    path("wallet/",views.wallet,name="wallet"),
    path("info/",views.info,name="info"),
    path('api/wallets/', get_wallets, name='get_wallets'),
     




]
