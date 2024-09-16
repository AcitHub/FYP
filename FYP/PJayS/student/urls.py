from django.urls import path
from .views import *

urlpatterns = [
    path('home/register_student/', register_student, name='register_student'),
    path('home/delete_student_page/', delete_student_page, name='delete_student_page'),
    path('home/delete_student/<int:member_id>/', delete_student, name='delete_student'),
    path('home/update_student_page/', update_student_page, name='update_student_page'),
    path('home/update_student_page/edit_student/<int:member_id>/', edit_student, name='edit_student'),
]
