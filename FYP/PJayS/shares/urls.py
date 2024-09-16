from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/saham_komuniti/', saham_komuniti, name='saham_komuniti'),
]