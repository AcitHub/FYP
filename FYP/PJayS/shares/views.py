from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F
from django.contrib import messages
from .form import Tambah_Share
from .models import Teacher, SahamTeacher
from student.models import Member

def share_page(request): 
    context = {
        # "saham" : SahamTeacher.objects.all(),
        "teacher" : Teacher.objects.all(),
        "member" : Member.objects.all(),
    }
    return render(request, 'saham/muka surat-saham komuniti.html', context)


def add_share_teacher_func(request, teacher_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)

    if request.method == 'POST':
        form = Tambah_Share(request.POST)
        if form.is_valid():
            new_modal_syer = form.cleaned_data['amount']

            # Update the Teacher model
            teacher.modal_syer += new_modal_syer  # Corrected line - Only add the new amount
            teacher.save()

            # Create a new SahamTeacher record
            SahamTeacher.objects.create(teacher=teacher, amount=new_modal_syer)

            messages.success(request, 'Share amount updated successfully.')
            return redirect('share_page')
        else:
            messages.error(request, f"There was an error adding share: {form.errors}")
    else:
        form = Tambah_Share()

    return render(request, 'saham/tambah-saham-kakitangan.html', {'form': form, 'teacher': teacher})

# pie chart saham cikgu
def saham_pie_chart(request):
    # Retrieve Saham data (adjust the query as needed)
    saham_data = Teacher.objects.all()

    # Calculate total saham (if needed)
    total_saham = Teacher.objects.aggregate(total=Teacher.modal_syer.Sum('value'))['total']

    return render(request, 'saham_pie_chart.html', {
        'saham_data': saham_data,
        'total_saham': total_saham,
    })