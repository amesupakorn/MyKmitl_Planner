# forms.py
from django import forms
from planner.models import Student, UniversityStaff

class ProfileForm(forms.ModelForm):

    class Meta:
        MAJOR_CHOICES = [
            ('Engineering', 'Faculty of Engineering'),
            ('Architecture_Art_Design', 'Faculty of Architecture, Art, and Design'),
            ('Industrial_Education', 'Faculty of Industrial Education and Technology'),
            ('Agricultural_Technology', 'Faculty of Agricultural Technology'),
            ('Science', 'Faculty of Science'),
            ('Information_Technology', 'School of Information Technology'),
            ('Food_Industry', 'Faculty of Food Industry'),
            ('Liberal_arts', 'Faculty of Liberal Arts'),
            ('Business_Administration', 'Faculty of Business Administration'),
            ('Medicine', 'Faculty of Medicine'),
            ('Dentistry', 'Faculty of Dentistry'),
            ('Materials_Innovation', 'College of Materials Innovation and Technology'),
            ('Advanced_Manufacturing', 'College of Advanced Manufacturing Innovation'),
            ('Aviation_Industry', 'International Academy of Aviation Industry'),
            ('Music_Engineering', 'College of Music Engineering'),
            ('Chumphon_Campus', 'Chumphon Khet Udomsak Campus, Chumphon Province'),
        ]
        
        model = Student
        fields = ['first_name', 'last_name', 'year_of_study', 'major', 'profile_picture']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add a first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add a last name'}),
            'year_of_study': forms.Select(attrs={'class': 'form-control'}),  
            'major': forms.Select(choices=MAJOR_CHOICES, attrs={'class': 'form-control'}), 
            'profile_picture': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

class ProfileStaff(forms.ModelForm):
    class Meta:
        
        DEPART_CHOICES = [
            ('Engineering', 'Faculty of Engineering'),
            ('Architecture_Art_Design', 'Faculty of Architecture, Art, and Design'),
            ('Industrial_Education', 'Faculty of Industrial Education and Technology'),
            ('Agricultural_Technology', 'Faculty of Agricultural Technology'),
            ('Science', 'Faculty of Science'),
            ('Information_Technology', 'School of Information Technology'),
            ('Food_Industry', 'Faculty of Food Industry'),
            ('Liberal_arts', 'Faculty of Liberal Arts'),
            ('Business_Administration', 'Faculty of Business Administration'),
            ('Medicine', 'Faculty of Medicine'),
            ('Dentistry', 'Faculty of Dentistry'),
            ('Materials_Innovation', 'College of Materials Innovation and Technology'),
            ('Advanced_Manufacturing', 'College of Advanced Manufacturing Innovation'),
            ('Aviation_Industry', 'International Academy of Aviation Industry'),
            ('Music_Engineering', 'College of Music Engineering'),
            ('Chumphon_Campus', 'Chumphon Khet Udomsak Campus, Chumphon Province'),
        ]
        
        model = UniversityStaff
        fields = ['first_name', 'last_name', 'email', 'department']
        widgets = {
            'department' : forms.Select(choices=DEPART_CHOICES, attrs={'class': 'form-control'}), 
        }