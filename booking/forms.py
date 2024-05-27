from django import forms
from django.utils import timezone

from booking.models import Application


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['departure', 'arrival', 'date']
        labels = {
            'departure': 'Точка отправления',
            'arrival': 'Точка прибытия',
            'date': 'Дата и время',
        }
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        departure = cleaned_data.get('departure')
        arrival = cleaned_data.get('arrival')
        date = self.cleaned_data.get('date')

        if departure and arrival and departure == arrival:
            raise forms.ValidationError("Точка отправления и точка прибытия не могут совпадать.")

        if date:
            min_date = timezone.now() + timezone.timedelta(hours=1)
            if date < min_date:
                raise forms.ValidationError("Не раньше, чем через час от текущего.")
        return cleaned_data
