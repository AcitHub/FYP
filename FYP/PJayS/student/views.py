from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .form import *

# Create your views here.
def register_student(request):
    if request.method == 'POST':
        form = Tambah_Student(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data successfully saved')
            return redirect('/home/register_student/')  # Replace with your success URL
        else:
            messages.error(request, f"There was an error in the data: {form.errors}")
    else:
        form = Tambah_Student()
    member = Member.objects.all()
    return render(request, 'student/muka surat-pelajar-tambah data.html', {'member' : member})

def delete_student(request, member_id):
    if request.method == "POST" and member_id:
        member = Member.objects.get(member_id=member_id)
        member.delete()
        messages.success(request, 'Data successfully deleted')
        return redirect('/home/delete_student_page/')

def delete_student_page(request):
    member = Member.objects.all()
    return render(request,'student/muka surat-pelajar-padam data.html', {'member' : member})

def update_student_page(request):
    member = Member.objects.all()
    return render(request, 'student/muka surat-pelajar-kemas kini data.html', {'member': member})

def edit_student(request, member_id):
    member = Member.objects.get(member_id=member_id)
    if request.method == 'POST':
        form = Tambah_Student(request.POST or None, instance=member)
        if form.is_valid():
            form.save()
            return redirect('/home/update_student_page/')
    else:
        form = Tambah_Student(instance=member)
    return render(request, 'student/update-page.html', {'member': member})
