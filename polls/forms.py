from django.forms import ModelForm
from .models import Choice, Encounter, Question


class EncounterForm(ModelForm):
    class Meta:
        model = Encounter
        fields = ['name', 'response', 'notes']
