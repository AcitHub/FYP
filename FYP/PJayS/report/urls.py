from django.urls import path
from .views import generate_report

urlpatterns = [
    path('/generate_report/', generate_report, name='generate_report'),
    # path('home/generate_report_view/', generate_report_view, name='generate_report_view'),

]
