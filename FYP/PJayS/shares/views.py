from django.shortcuts import render, redirect
from django.contrib import messages
from .form import Tambah_Share
from .models import Saham, Teacher, Member

def share_page(request):
    if request.method == 'POST':
        form = Tambah_Share(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Share added successfully.')
            return redirect('share_page')  # Redirect to a page showing the list of shares
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = Tambah_Share()

    context = {
        "saham" : Saham.objects.all(),
        "teacher" : Teacher.objects.all(),
        "member" : Member.objects.all(),
    }
    return render(request, 'saham/muka surat-saham komuniti.html', context)
