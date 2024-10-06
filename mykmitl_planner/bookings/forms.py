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


class FacilityForm(forms.ModelForm):

    class Meta:
        FACILITY_CHOICES = [
            ('opening', 'opening'),
            ('closing', 'closing')
        ]

        model = Facility
        fields = ['name', 'location', 'description', 'opening', 'closing', 'location', 'status', 'capacity', 'booking_status']
        widgets = {
            'opening': forms.TimeInput(attrs={'type': 'time'}),
            'closing': forms.TimeInput(attrs={'type': 'time'}),
            'status': forms.Select(choices=FACILITY_CHOICES, attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-lg',
                'rows': 2,
            }),
        }