from django.urls import path
from .views import (
    admin_login,
    home,
    logout_view,
    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView
)

urlpatterns = [
    path('login/', admin_login, name='login'),
    path('home/', home, name='home'),
    path('home/logout/', logout_view, name='logout'),
    path('home/password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('home/password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('home/reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('home/reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
