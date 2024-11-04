import pandas as pd
import json
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Member
from .form import TambahStudentForm
from .form import UpdateStudentForm
from django.db import transaction
from django.db.models import Sum

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
                # Read the Excel file into a DataFrame
                df = pd.read_excel(file)
                df.columns = df.columns.str.strip()  # Remove any leading/trailing spaces in column names
                df = df.rename(columns={"tarikh_dafatr": "tarikh_daftar"})  # Fix typo in column name

                # Define required columns and check if they are all present
                required_columns = ["Ic Pelajar", "Nama", "Jantina", "Alamat Rumah", "Tingkatan", "Kelas", "Ahli", "Status Pengambilan Saham", "Modal Syer", "Tarikh Daftar"]
                if not all(col in df.columns for col in required_columns):
                    missing_columns = [col for col in required_columns if col not in df.columns]
                    messages.error(request, f"Missing columns in the uploaded file: {', '.join(missing_columns)}")
                    return redirect('register_student_kumpulan_page')

                # Replace any NaN or missing values with "-"
                df = df.fillna('-')

                # Convert the "Tarikh Daftar" column from Excel serial numbers or incorrect formats
                def convert_date(value):
                    try:
                        # Check if the value is an Excel serial date (numeric)
                        if isinstance(value, (int, float)):
                            return pd.to_datetime("1899-12-30") + pd.to_timedelta(int(value), unit='D')
                        # Otherwise, try to parse as a standard date string
                        return pd.to_datetime(value).date()
                    except Exception:
                        return None  # Return None for invalid dates

                # Apply the date conversion and handle invalid dates
                df['Tarikh Daftar'] = df['Tarikh Daftar'].apply(convert_date)
                if df['Tarikh Daftar'].isnull().any():
                    messages.error(request, "Some dates in the 'Tarikh Daftar' column could not be converted. Please ensure all dates are valid.")
                    return redirect('register_student_kumpulan_page')

                # Begin transaction to ensure atomic save
                with transaction.atomic():
                    for _, row in df.iterrows():
                        # Create a new Member object with data or '-' for missing fields
                        Member.objects.create(
                            ic_pelajar=row.get('Ic Pelajar'),
                            nama=row.get('Nama'),
                            jantina=row.get('Jantina'),
                            status=row.get('Status Pengambilan Saham'),
                            alamat_rumah=row.get('Alamat Rumah'),
                            tingkatan=row.get('Tingkatan'),
                            kelas=row.get('Kelas'),
                            ahli=row.get('Ahli'),
                            modal_syer=row.get('Modal Syer'),
                            tarikh_daftar=row.get('Tarikh Daftar'),
                        )
                messages.success(request, 'Data successfully uploaded and saved.')
                return redirect('register_student_kumpulan_page')

            except Exception as e:
                messages.error(request, f"An error occurred while processing the file: {e}")
        else:
            messages.error(request, 'No file uploaded.')

    # Load all members to display on the page
    member = Member.objects.all()
    return render(request, 'student/muka surat-pelajar-tambah data-kumpulan.html', {'member': member})

def delete_student_page(request):
    if request.method == 'POST':
        selected_students = request.POST.getlist('selected_students[]')
        if selected_students:
            Member.objects.filter(member_id__in=selected_students).delete()
            messages.success(request, 'Selected students have been deleted.')
        else:
            messages.warning(request, 'No students selected for deletion.')

    member = Member.objects.all()
    return render(request, 'student/muka surat-pelajar-padam data.html', {'member': member})

def update_student_page(request):
    member = Member.objects.all()
    return render(request, 'student/muka surat-pelajar-kemas kini data.html', {'member': member})

def edit_student(request, member_id):
    try:
        # Attempt to retrieve the member by ID
        member = Member.objects.get(member_id=member_id)
    except Member.DoesNotExist:
        messages.error(request, 'The selected student does not exist.')
        return redirect('update_student_page')  # Redirect to the update student page

    if request.method == 'POST':
        # Create the form instance with the posted data and the member instance
        form = UpdateStudentForm(request.POST, instance=member)
        
        if form.is_valid():
            # Check if any changes were made
            if form.has_changed():
                # Save the form only if there are changes
                form.save()
                messages.success(request, 'Student data updated successfully.')
            else:
                # Notify that no changes were made
                messages.warning(request, 'No updates have been done as the values were the same.')

            return redirect('update_student_page')  # Redirect after handling the form submission
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
        form = UpdateStudentForm(instance=member)

    return render(request, 'student/update-page.html', {'form': form, 'member': member})

def update_student_kumpulan_page(request):
    if request.method == 'POST':
        new_tingkatan = request.POST.get('new_tingkatan')
        new_kelas = request.POST.get('new_kelas')
        new_status = request.POST.get('new_status')
        new_ahli = request.POST.get('new_ahli')

        selected_students = request.POST.getlist('selected_students[]')

        if selected_students:
            students_to_update = Member.objects.filter(member_id__in=selected_students)

            updated = False  

            if new_tingkatan and students_to_update.exclude(tingkatan=new_tingkatan).exists():
                students_to_update.update(tingkatan=new_tingkatan)
                updated = True

            if new_kelas and students_to_update.exclude(kelas=new_kelas).exists():
                students_to_update.update(kelas=new_kelas)
                updated = True

            if new_status and students_to_update.exclude(status=new_status).exists():
                students_to_update.update(status=new_status)
                updated = True

            if new_ahli and students_to_update.exclude(ahli=new_ahli).exists():
                students_to_update.update(ahli=new_ahli)
                updated = True

            if updated:
                messages.success(request, 'Selected students have been updated.')
            else:
                messages.warning(request, 'No updates were made as the values were the same.')
        else:
            messages.warning(request, 'No students selected for updating.')

        return redirect('update_student_kumpulan_page')

    member = Member.objects.all()

    return render(request, 'student/muka surat-pelajar-kemas kini-kumpulan.html', {'member': member})

def help_page(request):
    member = Member.objects.all()
    return render(request, 'student/laman-perlukan bantuan.html', {'member': member})

def profile_page(request):
    member = Member.objects.all()
    return render(request, 'student/laman-profil.html', {'member': member})

def data_student(request):
    # list all member
    member =  Member.objects.all()

    # total_student
    total_member = Member.objects.count()

    # total_saham
    total_saham_member = sum([member.modal_syer for member in Member.objects.all()])

    # Calculate total number of active and inactive students
    pelajar_aktif = Member.objects.filter(ahli="Aktif").count()
    pelajar_tidak_aktif = Member.objects.filter(ahli="Tidak Aktif").count()

    # Calculate total number of active and inactive share ownership
    saham_selesai = Member.objects.filter(status="Selesai").count()
    saham_belum_selesai = Member.objects.filter(status="Belum Selesai").count()

    # Prepare the data for the bar chart
    bar_chart_data = Member.objects.values('tingkatan').annotate(total_saham=Sum('modal_syer')).order_by('tingkatan')
    bar_chart_data_list = list(bar_chart_data)
    # Convert Decimal objects to float
    bar_chart_data_list = [{'tingkatan': item['tingkatan'], 'total_saham': float(item['total_saham'])} for item in bar_chart_data_list]

    context = {
        'saham_selesai': saham_selesai,
        'saham_belum_selesai': saham_belum_selesai,
        'pelajar_aktif': pelajar_aktif,
        'pelajar_tidak_aktif' : pelajar_tidak_aktif,
        'member': member,
        'total_saham_member' : total_saham_member,
        'total_member': total_member,
        "bar_chart_data": json.dumps(bar_chart_data_list),
    }
    return render(request, 'student/muka surat data-pelajar & saham.html', context)