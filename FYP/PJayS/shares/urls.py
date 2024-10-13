from django.urls import path
from .views import *

urlpatterns = [
    path('home/share_page/', share_page, name='share_page'),
    path('home/share_page/view_account_teacher/<int:teacher_id>/', view_account_teacher, name='view_account_teacher'),
    path('home/share_page/view_account_teacher/add_share_page_teacher/<int:teacher_id>/', add_share_teacher_func, name='add_share_page_teacher'),
    path('home/share_page/view_account_student/<str:member_id>/', view_account_student, name='view_account_student'),
    path('home/share_page/view_account_student/add_share_page_student/<str:member_id>/', add_share_student_func, name='add_share_page_student')
]
