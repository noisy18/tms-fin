from counterparties.models import CounterpartyCars

from django.forms import ModelForm
from django.forms import (
    TextInput,
    DateInput, 
    Textarea, 
    TimeInput, 
    CharField,
    )


class CounterPartyCarsForm(ModelForm):
    class Meta:
        model = CounterpartyCars
        fields = ['full_name', 'number_auto', 'vin_number', 'marka_auto', 'model_auto', 'release_date']

        widgets = {
            'full_name': TextInput(attrs={
                'class': 'input-container',
                'placeholder': 'Введите полное название автомобиля'
            }),

            'number_auto': TextInput(attrs={
                'class': 'input-container',
                'placeholder': 'Введите гос. номер авто'
            }),

            'vin_number': TextInput(attrs={
                'class': 'input-container',
                'placeholder': 'Введите VIN авто'
            }),

            'marka_auto': TextInput(attrs={
                'class': 'input-container',
                'placeholder': 'Введите марку авто'
            }),

            'model_auto': TextInput(attrs={
                'class': 'input-container',
                'placeholder': 'Введите модель авто'
            }),

            'release_date': TextInput(attrs={
                'class': 'input-container',
                'placeholder': 'Введите дату выпуска авто'
            }),
        }