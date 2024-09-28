from django import forms
from .models import Member

class TambahStudentForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['nama', 'ic_pelajar', 'jantina', 'kaum', 'agama', 'alamat_rumah', 'tingkatan', 'kelas', 'ahli', 'modal_syer', 'tarikh_daftar']
