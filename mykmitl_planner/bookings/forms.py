from django import forms
from planner.models import Event

class CreateEventForm(forms.ModelForm):
    class Meta:
        MAJOR_CHOICES = [
            ('ongoing', 'กำลังดำเนินการ'),
            ('upcoming', 'กำลังจะมาถึง'),
            ('completed', 'เสร็จสิ้นแล้ว')
        ]
        
        model = Event
        fields = ['event_image', 'name', 'description', 'start_time', 'end_time', 'location', 'status']
        widgets = {
            'status': forms.Select(choices=MAJOR_CHOICES, attrs={'class': 'form-control'}),
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }