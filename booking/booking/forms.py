from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_time', 'end_time']
        widgets = {
            'start_time': forms.DateInput(attrs={'type': 'text', 'class': 'form-control'}),
            'end_time': forms.DateInput(attrs={'type': 'text', 'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        
        if 'room' in self._errors:
            del self._errors['room']
            
        return cleaned_data