from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from .models import Encounter, Laborer, Team
from .view_models import DashboardViewModel
from .forms import EncounterForm
from django.utils import timezone
import geocoder


# Helper functions:
def get_laborer_id(request):
    user_id = request.user.id
    return Laborer.objects.get(user__id=user_id).id


def get_my_encounters(request):
    my_laborer_id = get_laborer_id(request)
    return Encounter.objects.filter(laborer_id=my_laborer_id)


def str_f(value):
    if value is None:
        return ''
    else:
        return str(value)

# todo: make this more complex and accurate (check for commas, etc)
def get_address_string(encounter: Encounter):
    full_address = ''
    street_part = ''
    if encounter.street_address_number is not None:
        street_part += (str(encounter.street_address_number) + ' ')
    if encounter.street_address_name is not None:
        street_part += (str(encounter.street_address_name) + ' ')
    if encounter.apt_or_unit is not None:
        street_part += (str(encounter.apt_or_unit) + ' ')

    if street_part != '':
        full_address += ', '

    if encounter.city is not None:
        full_address += (str(encounter.city) + ', ')

    if encounter.state is not None:
        full_address += (str(encounter.state) + ', ')

    if encounter.zip is not None:
        full_address += (str(encounter.zip))

    return full_address


def get_lat_lng_from_address(encounter: Encounter) -> (float, float):
    g = geocoder.google(get_address_string(encounter))
    print('LAT LONG = ' + str(g.lat) + ', ' + str(g.lng))
    return g.lat, g.lng

# Create your views here.

# todo: Django to pre-populate geolocation part of form based on most recent encounter geo data
def new_encounter(request):
    if request.method == "POST":
        form = EncounterForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.date_time = timezone.now()
            model_instance.laborer_id = get_laborer_id(request)
            model_instance.save()
            model_instance.lat, model_instance.lng = get_lat_lng_from_address(model_instance)

            return HttpResponseRedirect(reverse_lazy('npl:my_encounters'))

    else:
        form = EncounterForm()
        return render(request, 'npl/encounter_form.html', {'form': form})


class EncounterIndex(generic.ListView):
    template_name = 'npl/encounters.html'
    context_object_name = 'encounters_list'

    def get_queryset(self):
        """Return all encounters for this user."""
        my_encounters = get_my_encounters(self.request)
        return my_encounters.order_by('-date_time')


# todo: implement these views
class DashboardView(generic.View):
    # todo: figure out which metrics most important to show:
    model = DashboardViewModel


class TeamEncounters(generic.View):
    print('b')


class Settings(generic.View):
    print('c')


'''class AddEncounter(generic.edit.CreateView):
    model = Encounter
    fields = ['name', 'action_prayer', 'action_testimony',
              'action_gospel', 'response', 'street_address', 'apt_or_unit', 'city', 'state', 'zip', 'notes']
    success_url = reverse_lazy('npl:my_encounters')

    def form_valid(self, form):
        form.instance.date_time = timezone.now()
        return super().form_valid(form)'''


class DetailEncounter(generic.DetailView):
    model = Encounter
    fields = ['name', 'response', 'notes']
    template_name = 'npl/encounter_detail.html'


class DeleteEncounter(generic.DeleteView):
    model = Encounter
    template_name = 'npl/encounter_delete.html'
    success_url = reverse_lazy('npl:my_encounters')


class EditEncounter(generic.edit.UpdateView):
    model = Encounter
    fields = ['name', 'action_prayer', 'action_testimony',
              'action_gospel', 'response', 'street_address', 'apt_or_unit', 'city', 'state', 'zip', 'notes']
    success_url = reverse_lazy('npl:my_encounters')
    #todo: Change the url to go back to detail view?
