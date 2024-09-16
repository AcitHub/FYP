from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .form import *

# Create your views here.
def register_teacher(request):
    if request.method == 'POST':
        form = Tambah_Teacher(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data successfully saved')
            return redirect('/home/register_teacher/')  # Replace with your success URL
        else:
            messages.error(request, f"There was an error in the data: {form.errors}")
    else:
        form = Tambah_Teacher()
    teacher = Teacher.objects.all()
    return render(request, 'teacher/muka surat-cikgu-tambah data.html', {'teacher' : teacher})

def delete_teacher(request, teacher_id):
    if request.method == "POST" and teacher_id:
        teacher = Teacher.objects.get(teacher_id=teacher_id)
        teacher.delete()
        messages.success(request, 'Data successfully deleted')
        return redirect('/home/delete_teacher/')

def delete_teacher_page(request):
    teacher = Teacher.objects.all()
    return render(request,'teacher/muka surat-cikgu-padam data.html', {'teacher' : teacher})

def update_teacher_page(request):
    teacher = Teacher.objects.all()
    return render(request, 'teacher/muka surat-cikgu-kemas kini data.html', {'teacher': teacher})

def edit_teacher(request, teacher_id):
    teacher = Teacher.objects.get(teacher_id=teacher_id)
    if request.method == 'POST':
        form = Tambah_Teacher(request.POST or None, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('/home/update_teacher/')
    else:
        form = Tambah_Teacher(instance=teacher)
    return render(request, 'teacher/muka surat-cikgu-kemas kini data.html', {'teacher': teacher})
