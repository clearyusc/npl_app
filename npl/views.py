import json
from django.shortcuts import get_object_or_404, render
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from .models import Encounter, Laborer, Team
from .view_models import DashboardViewModel, EncounterPinViewModel
from .forms import EncounterForm
from . import utilities
from django.utils import timezone


# Helper functions:

class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, EncounterPinViewModel):
            return obj.__dict__
        elif isinstance(obj, DashboardViewModel):
            return obj.__dict__
        return super().default(obj)


def get_laborer_id(request):
    user_id = request.user.id
    return Laborer.objects.get(user__id=user_id).id


def get_my_encounters(request):
    my_laborer_id = get_laborer_id(request)
    return Encounter.objects.filter(laborer_id=my_laborer_id)


# Create your views here.


def new_encounter(request):
    if request.method == "POST":
        form = EncounterForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.date_time = timezone.now()
            model_instance.laborer_id = get_laborer_id(request)
            model_instance.lat, model_instance.lng = utilities.get_lat_lng_from_address(model_instance)
            model_instance.response_description = utilities.get_response_description(model_instance.response)
            model_instance.full_address = utilities.smart_get_address_string(model_instance)
            model_instance.save()

            return HttpResponseRedirect(reverse_lazy('npl:my_encounters'))

    else:
        recent = get_my_encounters(request).order_by('-date_time')[0]
        form = EncounterForm(initial={'street_address_name': recent.street_address_name,
                                      'city': recent.city,
                                      'state': recent.state,
                                      'zip': recent.zip})
        return render(request, 'npl/encounter_form.html', {'form': form})


def edit_encounter(request, pk):
    encounter = get_my_encounters(request).get(pk=pk)

    if request.method == "POST":
        form = EncounterForm(request.POST, instance=encounter)
        if form.is_valid():
            model_instance = form.save(commit=False)

            # Need to update these every time in case the data changes:
            if model_instance.lat != encounter.lat or model_instance.lng != encounter.lng:
                model_instance.lat, model_instance.lng = utilities.get_lat_lng_from_address(model_instance)
            if model_instance.response != encounter.response:
                model_instance.response_description = utilities.get_response_description(model_instance.response)

            model_instance.full_address = utilities.smart_get_address_string(model_instance)

            model_instance.save()

            return HttpResponseRedirect(reverse_lazy('npl:my_encounters'))
    else:
        form = EncounterForm(instance=encounter)

        return render(request, 'npl/encounter_form.html', {'form': form})


class EncounterIndexList(generic.ListView):
    template_name = 'npl/encounters.html'
    context_object_name = 'encounters_list'

    def get_queryset(self):
        """Return all encounters for this user."""
        my_encounters = get_my_encounters(self.request)
        return my_encounters.order_by('-date_time')


def encounter_map(request):
    encounter_pins = []
    my_encounters = get_my_encounters(request).order_by('-date_time')
    for encounter in my_encounters:
        if encounter.lat is not None and encounter.lng is not None:
            encounter_pins.append(EncounterPinViewModel(encounter))

    _json = json.dumps(encounter_pins, cls=LazyEncoder)
    if encounter_pins is None:  # default map center shows the entire US in view
        _map_center = json.dumps({'lat': 39.8283, 'lng': -98.5795, 'zoom': 4})
    else:
        _map_center = json.dumps({'lat': encounter_pins[0].lat, 'lng': encounter_pins[0].lng, 'zoom': 12})

    return render(request, 'npl/encounters_map.html', {'json': _json, 'map_center': _map_center})


# todo: change view type?
def view_dashboard(request):
    # todo: figure out which metrics most important to show:
    dashboard_vm = DashboardViewModel(get_my_encounters(request))
    fields = ['num_encounters']

    _json = json.dumps(dashboard_vm, cls=LazyEncoder)
    print('dashbaord vm = ' + str(_json))
    encounters_by_week = json.dumps({'num_encounters': dashboard_vm.num_encounters_by_week,
                                     'num_red_lights': dashboard_vm.num_red_lights_by_week})
    print('e by w = ' + str(encounters_by_week))
    return render(request, 'npl/dashboard.html', {'django_json': _json, 'encounters_by_week': encounters_by_week})


class TeamEncounters(generic.View):
    print('b')


class Settings(generic.View):
    print('c')


class DetailEncounter(generic.DetailView):
    model = Encounter
    fields = ['name', 'response_description', 'notes']
    template_name = 'npl/encounter_detail.html'


class DeleteEncounter(generic.DeleteView):
    model = Encounter
    template_name = 'npl/encounter_delete.html'
    success_url = reverse_lazy('npl:my_encounters')


class EditEncounter(generic.edit.UpdateView):
    model = Encounter
    fields = ['name', 'action_prayer', 'action_testimony',
              'action_gospel', 'response', 'street_address_number', 'street_address_name',
              'apt_or_unit', 'city', 'state', 'zip', 'notes']

    success_url = reverse_lazy('npl:my_encounters')
    #todo: Change the url to go back to detail view?
