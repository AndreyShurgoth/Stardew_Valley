# forms.py
from django import forms
from .parameters import PARAMETERS

class CropForm(forms.Form):
    SEASON_CHOICES = [
        ('spring', 'Весна'),
        ('summer', 'Літо'),
        ('autumn', 'Осінь'),
        ('winter', 'Зима'),
    ]
    
    season = forms.ChoiceField(choices=SEASON_CHOICES)
    culture = forms.ChoiceField(choices=[])
    number_of_beds = forms.IntegerField(min_value=1, initial=1)

    def update_culture_choices(self, season):
        # Оновлюємо список культур залежно від вибраного сезону
        culture_choices = [(key, key.capitalize()) for key in PARAMETERS.get(season, {}).keys()]
        self.fields['culture'].choices = culture_choices
