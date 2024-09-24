from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from student.models import*
from teacher.models import*

def admin_login(request):
    if request.user.is_authenticated:
        return redirect('/home/')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')  # Corrected spelling

        user = authenticate(username=username, password=password)  # Corrected usage

        if user:
            if user.is_superuser:
                login(request, user)
                return redirect('/home/')
            else:
                messages.info(request, 'You are not an admin user.')
                return redirect('/login/')
        else:
            messages.info(request, 'Invalid username or password')
            return redirect('/login/')

    return render(request, 'login/pages-login-signup.html')

def home(request):
    if request.user.is_authenticated is not True: 
        return redirect('/login/')
    
    member = Member.objects.count()
    teacher  = Teacher.objects.count()
    return render(request, 'login/laman utama-papan pemuka analisis.html', {'member':member, 'teacher':teacher})


def logout_view(request):
    logout(request)
    return redirect('/login/')
