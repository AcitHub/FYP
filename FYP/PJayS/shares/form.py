# forms.py
from django import forms
from .models import SahamTeacher

class Tambah_Share(forms.ModelForm):

    class Meta:
        model = SahamTeacher
        fields = ['amount']