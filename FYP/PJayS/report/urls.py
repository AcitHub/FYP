from django.urls import path
from .views import generate_report

urlpatterns = [
    path('home/generate_report/', generate_report, name='generate_report'),

]
