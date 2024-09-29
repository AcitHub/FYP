import pandas as pd
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Member
from .form import TambahStudentForm, UpdateStudentForm

def get_all_members():
    """Helper function to get all members."""
    return Member.objects.all()

def register_student(request):
    if request.method == 'POST':
        form = TambahStudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data successfully saved.')
            return redirect('register_student')
        else:
            # Collect and display friendly error messages
            error_messages = form.errors
            friendly_errors = []
            for field, errors in error_messages.items():
                field_name = form[field].label
                for error in errors:
                    friendly_errors.append(f"{field_name}: {error}")
            if friendly_errors:
                messages.error(request, "Please correct the following errors: " + ", ".join(friendly_errors))

    else:
        form = TambahStudentForm()

    member = get_all_members()
    context = {
        'member': member,
    }
    return render(request, 'student/muka surat-pelajar-tambah data.html', context)

def register_student_kumpulan_page(request):
    if request.method == 'POST':
        file = request.FILES.get('file_upload')
        if file:
            try:
                df = pd.read_excel(file)
                for _, row in df.iterrows():
                    Member.objects.update_or_create(
                        member_id=row.get('ID member'),
                        defaults={
                            'ic_pelajar': row.get('No. IC'),
                            'nama': row.get('Nama'),
                            'jantina': row.get('Jantina'),
                            'kaum': row.get('Kaum'),
                            'agama': row.get('Agama'),
                            'alamat_rumah': row.get('Alamat Rumah'),
                            'tingkatan': row.get('Tingkatan'),
                            'kelas': row.get('Kelas'),
                            'ahli': row.get('Ahli'),
                            'modal_syer': row.get('Modal Syer(RM)'),
                            'tarikh_daftar': row.get('Tarik Pendaftaran'),
                        }
                    )
                messages.success(request, 'Data successfully uploaded and saved.')
                return redirect('register_student_kumpulan_page')
            except Exception as e:
                messages.error(request, f"An error occurred while processing the file: {e}")
        else:
            messages.error(request, 'No file uploaded.')

    member = get_all_members()
    return render(request, 'student/muka surat-pelajar-tambah data-kumpulan.html', {'member': member})

def delete_student_page(request):
    if request.method == 'POST':
        selected_students = request.POST.getlist('selected_students[]')
        if selected_students:
            Member.objects.filter(member_id__in=selected_students).delete()
            messages.success(request, 'Selected students have been deleted.')
        else:
            messages.warning(request, 'No students selected for deletion.')

    member = get_all_members()
    return render(request, 'student/muka surat-pelajar-padam data.html', {'member': member})

def update_student_page(request):
    member = get_all_members()
    return render(request, 'student/muka surat-pelajar-kemas kini data.html', {'member': member})

def edit_student(request, member_id):
    try:
        member = Member.objects.get(member_id=member_id)
    except Member.DoesNotExist:
        messages.error(request, 'The selected student does not exist.')
        return redirect('update_student_page')

    if request.method == 'POST':
        form = UpdateStudentForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student data updated successfully.')
            return redirect('update_student_page')
        else:
            messages.error(request, f"There was an error updating the data: {form.errors}")
    else:
        form = UpdateStudentForm(instance=member)

    return render(request, 'student/update-page.html', {'form': form, 'member': member})

def update_student_kumpulan_page(request):
    if request.method == 'POST':
        new_tingkatan = request.POST.get('new_tingkatan')
        new_kelas = request.POST.get('new_kelas')
        selected_students = request.POST.getlist('selected_students[]')

        if selected_students:
            students_to_update = Member.objects.filter(member_id__in=selected_students)
            try:
                if new_tingkatan:
                    students_to_update.update(tingkatan=new_tingkatan)
                if new_kelas:
                    students_to_update.update(kelas=new_kelas)

                messages.success(request, 'Selected students have been updated.')
                return redirect('update_student_kumpulan_page')
            except Exception as e:
                messages.error(request, f"Error updating students: {e}")
        else:
            messages.warning(request, 'No students selected for updating.')

    member = get_all_members()
    return render(request, 'student/muka surat-pelajar-kemas kini-kumpulan.html', {'member': member})

def generate_student_page(request):
    member = get_all_members()
    return render(request, 'student/muka surat-Hasilkan Laporan.html', {'member': member})
