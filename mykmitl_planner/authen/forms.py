# forms.py
from django import forms
from planner.models import Student

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'year_of_study', 'major', 'profile_picture']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add a first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add a last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Add an email'}),
            'year_of_study': forms.Select(attrs={'class': 'form-control'}),  # ใช้ Select widget สำหรับ choices
            'major': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add a major'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

