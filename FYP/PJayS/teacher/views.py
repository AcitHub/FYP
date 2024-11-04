from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .form import *
from shares.models import SahamTeacher
import json
from django.db.models import Sum

# Create your views here.
def register_teacher(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data successfully saved.')
            return redirect('register_teacher')  # Replace with your success URL
        else:
            # Collect and display user-friendly error messages
            error_messages = form.errors
            friendly_errors = []
            for field, errors in error_messages.items():
                field_name = form[field].label if form[field].label else field  # Get the field label
                for error in errors:
                    friendly_errors.append(f"{field_name}: {error}")
            if friendly_errors:
                messages.error(request, "Please correct the following errors: " + ", ".join(friendly_errors))
    else:
        form = TeacherForm()

    teacher = Teacher.objects.all()
    return render(request, 'teacher/muka surat-cikgu-tambah data.html', {'form': form, 'teacher': teacher})

def delete_teacher(request, teacher_id):
    if request.method == "POST" and teacher_id:
        teacher = Teacher.objects.get(teacher_id=teacher_id)
        teacher.delete()
        messages.success(request, 'Data successfully deleted')
        return redirect('/home/delete_teacher_page/')

def delete_teacher_page(request):
    teacher = Teacher.objects.all()
    return render(request,'teacher/muka surat-cikgu-padam data.html', {'teacher' : teacher})

def update_teacher_page(request):
    teacher = Teacher.objects.all()
    return render(request, 'teacher/muka surat-cikgu-kemas kini data.html', {'teacher': teacher})

def edit_teacher(request, teacher_id):
    try:
        # Attempt to retrieve the member by ID
        teacher = Teacher.objects.get(teacher_id=teacher_id)
    except Teacher.DoesNotExist:
        messages.error(request, 'The selected Teacher does not exist.')
        return redirect('update_teacher_page')  # Redirect to the update student page

    if request.method == 'POST':
        # Create the form instance with the posted data and the member instance
        form = UpdateTeacherForm(request.POST, instance=teacher)
        
        if form.is_valid():
            # Check if any changes were made
            if form.has_changed():
                # Save the form only if there are changes
                form.save()
                messages.success(request, 'Teacher data updated successfully.')
            else:
                # Notify that no changes were made
                messages.warning(request, 'No updates have been done as the values were the same.')

            return redirect('update_teacher_page')  # Redirect after handling the form submission
        else:
            # If there are form errors, display them to the user
            error_messages = form.errors
            friendly_errors = []
            for field, errors in error_messages.items():
                field_name = form[field].label
                for error in errors:
                    friendly_errors.append(f"{field_name}: {error}")
            if friendly_errors:
                messages.error(request, "Please correct the following errors: " + ", ".join(friendly_errors))
    else:
        # If not a POST request, create a form instance with the current member data
        form = UpdateTeacherForm(instance=teacher)

    return render(request, 'teacher/update-cikgu page.html', {'form': form, 'teacher': teacher})

def data_teacher(request):
    # list all teachers
    teacher = Teacher.objects.all()

    # total teacher
    total_teacher = Teacher.objects.count()

    # total saham teacher
    total_saham_teacher = sum([teacher.modal_syer for teacher in Teacher.objects.all()])

    # Calculate total number of active and inactive teacher
    kakitangan_aktif = Teacher.objects.filter(ahli="Aktif").count()
    kakitangan_tidak_aktif = Teacher.objects.filter(ahli="Tidak Aktif").count()

    # Calculate total number of dah ambil saham and belum ambil saham
    saham_selesai = Teacher.objects.filter(status="Selesai").count()
    saham_belum_selesai = Teacher.objects.filter(status="Belum Selesai").count()

    # Updated Query
    transaction_data = (
        SahamTeacher.objects
        .select_related('teacher')  # Fetch related Teacher objects
        .values('date_saham_added', 'teacher__nama')  # Access the teacher's name correctly
        .annotate(total_saham=Sum('amount'))
        .order_by('date_saham_added')
    )

    # Prepare the data for the line chart
    line_chart_data = [
        {
            'date_time': item['date_saham_added'].strftime('%Y-%m-%d %H:%M:%S'),
            'total_saham': float(item['total_saham'] or 0),  # Ensure total_saham is a float
            'teacher_name': item['teacher__nama']  # Correctly access teacher's name
        }
        for item in transaction_data
    ]

    context = {
        'saham_selesai': saham_selesai,
        'saham_belum_selesai': saham_belum_selesai,
        'kakitangan_aktif': kakitangan_aktif,
        'kakitangan_tidak_aktif' : kakitangan_tidak_aktif,
        "total_saham_teacher":  total_saham_teacher,
        "total_teacher": total_teacher,
        "teacher" : teacher,
        "line_chart_data": json.dumps(line_chart_data)
    }
    return render(request,  'teacher/muka surat data-cikgu & saham.html', context)