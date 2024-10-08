from django.urls import path
from .views import *

urlpatterns = [
    path('home/share_page/', share_page, name='share_page'),
    path('home/add_share_page/<int:teacher_id>/',  add_share_teacher_func, name='add_share_page'),
]
