from django import forms
from planner.models import Event, Facility

class CreateEventForm(forms.ModelForm):

    class Meta:
        facility = forms.ModelMultipleChoiceField(
        queryset=Facility.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="สถานที่จัดกิจกรรม"
        )

        MAJOR_CHOICES = [
            ('ongoing', 'ongoing'),
            ('upcoming', 'upcoming'),
            ('completed', 'completed')
        ]
        
        model = Event
        fields = ['event_image', 'name', 'description', 'start_time', 'end_time', 'facility', 'status', 'participants']
        widgets = {
            'status': forms.Select(choices=MAJOR_CHOICES, attrs={'class': 'form-control'}),
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

