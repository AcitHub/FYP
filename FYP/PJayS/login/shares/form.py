# forms.py
from django import forms
from .models import Saham

class Tambah_Share(forms.ModelForm):
    class Meta:
        model = Saham
        fields = ['student', 'teacher', 'share_amount', 'share_type']

    def clean(self):
        cleaned_data = super().clean()
        student = cleaned_data.get('student')
        teacher = cleaned_data.get('teacher')

        if not student and not teacher:
            raise forms.ValidationError('Either a student or a teacher must be selected.')
        if student and teacher:
            raise forms.ValidationError('Only one of student or teacher can be selected.')

        return cleaned_data
