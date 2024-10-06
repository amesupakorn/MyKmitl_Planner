from django import forms
from planner.models import Schedule

class CalendarForm(forms.ModelForm):
    
    class Meta:
        model = Schedule
        field = ['facility', 'event', 'title', 'description', 'start_time', 'end_time', 'color']
        exclude = ['student']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'color': forms.TextInput(attrs={'type': 'color'}),
        }
