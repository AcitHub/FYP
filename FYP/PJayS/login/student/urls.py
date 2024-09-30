from django.urls import path
from .views import register_student, delete_student_page, update_student_page, edit_student, update_student_kumpulan_page, register_student_kumpulan_page, generate_student_page

urlpatterns = [
    path('home/register_student/', register_student, name='register_student'),
    path('home/register_student_kumpulan_page/', register_student_kumpulan_page, name='register_student_kumpulan_page'),
    path('home/delete_student_page/', delete_student_page, name='delete_student_page'),
    path('home/update_student_page/', update_student_page, name='update_student_page'),
    path('home/edit_student/<str:member_id>/', edit_student, name='edit_student'),
    path('home/update_student_kumpulan_page/', update_student_kumpulan_page, name='update_student_kumpulan_page'),
    path('home/generate_student_page/', generate_student_page, name='generate_student_page'),

]
