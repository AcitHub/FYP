from django.urls import path
from .views import *

urlpatterns = [
    path('home/register_teacher/', register_teacher, name='register_teacher'),
    path('home/delete_teacher_page/', delete_teacher_page, name='delete_teacher_page'),
    path('home/delete_teacher/<int:teacher_id>/', delete_teacher, name='delete_teacher'),
    path('home/update_teacher_page/', update_teacher_page, name='update_teacher_page'),
    path('home/update_teacher_page/edit_teacher/<int:teacher_id>/', edit_teacher, name='edit_teacher'),
]
