from django import forms
from .models import *

class Tambah_Teacher(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'