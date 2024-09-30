from django import forms
from .models import Member

class UpdateStudentForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = [
            'nama', 
            'ic_pelajar', 
            'jantina', 
            'kaum', 
            'agama', 
            'alamat_rumah', 
            'tingkatan', 
            'kelas', 
            'ahli', 
            'modal_syer', 
            'tarikh_daftar'
        ]

class TambahStudentForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = [
            'nama', 
            'ic_pelajar', 
            'jantina', 
            'kaum', 
            'agama', 
            'alamat_rumah', 
            'tingkatan', 
            'kelas', 
            'ahli', 
            'modal_syer', 
            'tarikh_daftar'
        ]

    def clean_ic_pelajar(self):
        ic_pelajar = self.cleaned_data.get('ic_pelajar')
        if Member.objects.filter(ic_pelajar=ic_pelajar).exists():
            raise forms.ValidationError("This IC number is already registered. Please use a different one.")
        return ic_pelajar

    def clean_nama(self):
        nama = self.cleaned_data.get('nama')
        if not nama:
            raise forms.ValidationError("Please enter a name.")
        return nama
