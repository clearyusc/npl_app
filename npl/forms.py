from django.forms import ModelForm
from .models import Encounter


class EncounterForm(ModelForm):
    class Meta:
        model = Encounter
        fields = ['name', 'action_prayer', 'action_testimony', 'action_gospel', 'response',
                  'street_address', 'apt_or_unit', 'city', 'state', 'zip', 'notes']
