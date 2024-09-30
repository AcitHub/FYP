from django.urls import path
from .views import share_page

urlpatterns = [
    path('home/share_page/', share_page, name='share_page'),

]
