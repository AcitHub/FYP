from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from student.models import*
from teacher.models import*
import json
from django.db.models import Sum
from django.db.models.functions import TruncMonth

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
    
    # total of teacher and student
    member = Member.objects.count()
    teacher  = Teacher.objects.count()

    # total saham teacher and student
    teacher_total = sum([teacher.modal_syer for teacher in Teacher.objects.all()])
    member_total = sum([member.modal_syer for member in Member.objects.all()])

    # Prepare the data for the line chart
    line_chart_data = Member.objects.annotate(month_year=TruncMonth('tarikh_daftar')).values('month_year').annotate(total_modal_syer=Sum('modal_syer')).order_by('month_year')
    line_chart_data_list = list(line_chart_data)
    # Convert Decimal objects to float
    line_chart_data_list = [{'month_year': item['month_year'].strftime('%b %Y'), 'total_modal_syer': float(item['total_modal_syer'])} for item in line_chart_data_list]

    context = {
        "member": member,
        "teacher": teacher,
        "teacher_total": teacher_total,
        "member_total": member_total,
        "line_chart_data": json.dumps(line_chart_data_list)
    }
    return render(request, 'login/laman utama-papan pemuka analisis.html', context)


def logout_view(request):
    logout(request)
    return redirect('/login/')
