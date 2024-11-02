from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('login/', admin_login ,name='login'),
    path('home/', home , name='home'),
    path('logout/', logout_view, name='logout'),
    path('about/', about_view , name='about'),
    path('organization_chart/', organization_chart_view , name='organization_chart')
] 
