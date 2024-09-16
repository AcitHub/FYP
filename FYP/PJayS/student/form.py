from django import forms
from .models import *

class Tambah_Student(forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'