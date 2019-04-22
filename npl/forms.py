from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Encounter, Team, Laborer
from django.utils import timezone


class EncounterForm(ModelForm):
    class Meta:
        model = Encounter
        fields = ['name', 'action_prayer', 'action_testimony', 'action_gospel', 'response',
                  'street_address_number', 'street_address_name', 'apt_or_unit', 'city', 'state', 'zip', 'notes']

    def __init__(self, *args, **kwargs):
        super(EncounterForm, self).__init__(*args, **kwargs)
        #self.fields['name'].widget.attrs.update({'class': 'test_this_class'})
        self.fields['action_prayer'].widget.attrs.update({'class': 'btn btn-secondary'})


class TeamForm(ModelForm):
    class Meta:
        model = Team
        fields = ['team_name']

    #def team_name_already_exists(self, name):
    #    exists_already = Team.objects.get_or_create(team_name=name)[1]
    #    return exists_already


class CreateUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    repeat_password = forms.CharField(widget=forms.PasswordInput)
    # Here we can add the extra form fields that we will use to create another model object
    # phone_number = forms.CharField(required=False)
    # date_of_birth = forms.CharField(required=False)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
        ]


'''class LaborerCreationForm(UserCreationForm):
    # future opps: Add fields as appropriate for your Profile mode
    #job_title = forms.CharField(max_length=100, required=True)
    age = forms.IntegerField(required=True)

    fields = ['username', ]

    class Meta:
        model = User

    def save(self, commit=True):
        if not commit:
            raise NotImplementedError("Can't create User and UserProfile without database save")
        user = super(LaborerCreationForm, self).save(commit=True)
        user_profile = Laborer(user=user, creation_date=timezone.now())
        user_profile.save()
        return user, user_profile'''
