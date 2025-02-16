from django import forms
from .models import Events

class EventForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = [
            'date',
            'employee',
            'location',
            'category',
            'event_name',
            'region',
            'city',
            'VPN',
            'adults',
            'university_students',
            'college_students',
            'school',
            'children',
            'pensioners',
            'socially_supported_children',
            'socially_supported_adult',
            'pushkn_cards',
            'indigenous_children',
            'indigenous_adult',
            'autism_spectrum_children',
            'svo_children',
            'preferential',
            'Comments'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date:
            return date
        raise forms.ValidationError('Введите корректную дату')
