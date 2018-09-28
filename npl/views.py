import json
import csv
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib import auth
from django.http import HttpResponseRedirect
from .forms import CreateUserForm
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.edit import FormView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

from .models import Encounter, Laborer, Team
from .view_models import DashboardViewModel, EncounterPinViewModel
from .admin import EncounterResource
from .forms import EncounterForm, TeamForm, CreateUserForm
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


def get_laborer(request):
    user_id = request.user.id
    return Laborer.objects.get(user__id=user_id)


def get_my_encounters(request):
    my_laborer_id = get_laborer_id(request)
    return Encounter.objects.filter(laborer_id=my_laborer_id)


def get_team_encounters(team_id):
    laborer_id_list = []

    team = Team.objects.filter(id=team_id).first()
    team_members = team.members.all()

    # todo: OPTIMIZE THIS QUERY!
    # todo: account for time when people were not with that team

    for member in team_members:
        laborer_id = Laborer.objects.filter(id=member.id).first()
        laborer_id_list.append(laborer_id)

    return Encounter.objects.filter(laborer_id__in=laborer_id_list)

# Create your views here.


def new_encounter(request):
    if request.method == "POST":
        form = EncounterForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.date_time = timezone.now()
            model_instance.laborer_id = get_laborer_id(request)
            model_instance.lat, model_instance.lng = utilities.get_lat_lng_from_address(
                model_instance)
            model_instance.response_description = utilities.get_response_description(
                model_instance.response)
            model_instance.full_address = utilities.smart_get_address_string(
                model_instance)
            model_instance.save()

            return HttpResponseRedirect(reverse_lazy('npl:my_encounters'))

    else:
        my_encounters = get_my_encounters(request)
        if my_encounters.exists():
            print('IT EXISTS?!?!?!?!?!?!?!?!')
            recent = my_encounters.order_by('-date_time')[0]
            form = EncounterForm(initial={'street_address_name': recent.street_address_name,
                                          'city': recent.city,
                                          'state': recent.state,
                                          'zip': recent.zip})
        else:
            form = EncounterForm(initial={'street_address_name': '',
                                          'city': '',
                                          'state': '',
                                          'zip': ''})

        return render(request, 'npl/encounter_form.html', {'form': form})


def edit_encounter(request, pk):
    encounter = get_my_encounters(request).get(pk=pk)

    if request.method == "POST":
        form = EncounterForm(request.POST, instance=encounter)
        if form.is_valid():
            model_instance = form.save(commit=False)

            # Need to update these every time in case the data changes:
            if model_instance.lat != encounter.lat or model_instance.lng != encounter.lng:
                model_instance.lat, model_instance.lng = utilities.get_lat_lng_from_address(
                    model_instance)
            if model_instance.response != encounter.response:
                model_instance.response_description = utilities.get_response_description(
                    model_instance.response)

            model_instance.full_address = utilities.smart_get_address_string(
                model_instance)

            model_instance.save()

            return HttpResponseRedirect(reverse_lazy('npl:my_encounters'))
    else:
        form = EncounterForm(instance=encounter)

        return render(request, 'npl/encounter_form.html', {'form': form})


class EncounterIndexList(generic.ListView):
    template_name = 'npl/encounters.html'
    context_object_name = 'encounters_list'

    def get(self, request, *args, **kwargs):
        my_encounters = get_my_encounters(self.request)
        my_encounters.order_by('-date_time')
        context = {'encounters_list': my_encounters,
                   'team_encounter_mode': False}
        return render(request, "npl/encounters.html", context=context)


class TeamEncounterIndexList(generic.ListView):
    template_name = 'npl/encounters.html'
    context_object_name = 'encounters_list'

    def get(self, request, *args, **kwargs):
        team_encounters = get_team_encounters(kwargs['pk'])
        team_encounters.order_by('-date_time')
        context = {'encounters_list': team_encounters,
                   'team_encounter_mode': True}
        return render(request, "npl/encounters.html", context=context)


def _export_encounters_to_csv_file(queryset):
    dataset = EncounterResource().export(queryset=queryset)

    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="my_encounters.csv"'

    return response


def export_my_encounters(request):
    my_encounters = get_my_encounters(request).order_by('-date_time')
    return _export_encounters_to_csv_file(my_encounters)


def export_team_encounters(request, pk):
    team_encounters = get_team_encounters(pk)
    return _export_encounters_to_csv_file(team_encounters)


def _render_encounter_map(request, encounters, title):
    encounter_pins = []
    default_map_center = json.dumps(
        {'lat': 39.8283, 'lng': -98.5795, 'zoom': 4})

    # Check if the user has logged any encounters yet!
    if not encounters.exists():
        return render(request, 'npl/encounters_map.html', {'json': 'no_encounters', 'map_center': default_map_center})

    for encounter in encounters:
        if encounter.lat is not None and encounter.lng is not None:
            encounter_pins.append(EncounterPinViewModel(encounter))

    _json = json.dumps(encounter_pins, cls=LazyEncoder)
    if encounter_pins is None:  # default map center shows the entire US in view
        _map_center = default_map_center
    else:
        _map_center = json.dumps(
            {'lat': encounter_pins[0].lat, 'lng': encounter_pins[0].lng, 'zoom': 12})

    return render(request, 'npl/encounters_map.html', {'title': title, 'json': _json, 'map_center': _map_center})


def encounter_map(request):
    my_encounters = get_my_encounters(request).order_by('-date_time')
    return _render_encounter_map(request, my_encounters, title='My Encounters')


def team_encounter_map(request, pk):
    team_encounters = get_team_encounters(pk).order_by('-date_time')
    team = Team.objects.get(id=pk)

    return _render_encounter_map(request, team_encounters, title=team.team_name)


def view_my_dashboard(request):
    # todo: figure out which metrics most important to show:
    my_encounters = get_my_encounters(request)

    if not my_encounters.exists():
        return render(request, 'npl/dashboard.html', {'title': 'My', 'dashboard_empty': True,
                                                      'django_json': '', 'encounters_by_week': ''})

    dashboard_vm = DashboardViewModel(get_my_encounters(request))

    _json = json.dumps(dashboard_vm, cls=LazyEncoder)
    encounters_by_week = json.dumps({'num_encounters': dashboard_vm.num_encounters_by_week,
                                     'num_red_lights': dashboard_vm.num_red_lights_by_week})
    return render(request, 'npl/dashboard.html', {'title': 'My', 'dashboard_empty': False,
                                                  'django_json': _json, 'encounters_by_week': encounters_by_week})


def view_settings(request):
    my_laborer_id = get_laborer_id(request)
    my_teams_list = Team.objects.all().filter(members__id=my_laborer_id)

    other_team_members_list = []

    for team in my_teams_list:
        other_team_members = team.members.all().exclude(id=my_laborer_id)
        other_team_members_list.append(other_team_members)

    #    my_teams_list = Team.objects.members.all().filter(laborer_id=get_laborer_id(request))
    print('my team MEMBERS = {}'.format(other_team_members_list))
    return render(request, 'npl/settings.html', {'my_teams_list': my_teams_list,
                                                 'other_team_members_list': other_team_members_list,
                                                 })


def view_team(request, pk):
    team = Team.objects.filter(id=pk).first()
    members = team.members.all()

    return render(request, 'npl/team_detail.html', {'team': team, 'team_members': members})


def view_team_dashboard(request, pk):
    team_encounters = get_team_encounters(pk)
    team = Team.objects.filter(id=pk).first()

    if not team_encounters.exists():
        return render(request, 'npl/dashboard.html', {'title': 'My', 'dashboard_empty': True,
                                                      'django_json': '', 'encounters_by_week': ''})

    # todo: figure out which metrics most important to show:
    dashboard_vm = DashboardViewModel(team_encounters)

    _json = json.dumps(dashboard_vm, cls=LazyEncoder)
    encounters_by_week = json.dumps({'num_encounters': dashboard_vm.num_encounters_by_week,
                                     'num_red_lights': dashboard_vm.num_red_lights_by_week})
    return render(request, 'npl/dashboard.html', {'title': team.team_name, 'dashboard_empty': False,
                                                  'django_json': _json, 'encounters_by_week': encounters_by_week})


def create_team(request):
    if request.method == "POST":
        form = TeamForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.creation_date = timezone.now()
            team_exists = Team.objects.filter(
                team_name=model_instance.team_name).count() > 0
            if team_exists:
                return render(request, 'npl/team_form.html', {'form': form, 'error': 'A team with that name already exists!'})
            else:
                model_instance.save()
                # the creator of the team automatically joins
                model_instance.members.add(get_laborer(request))
                return HttpResponseRedirect(reverse_lazy('npl:settings'))

        else:
            return render(request, 'npl/team_form.html', {'form': form, 'error': 'Form is invalid!'})

    else:
        form = TeamForm(request.POST)
        return render(request, 'npl/team_form.html', {'form': form})


def join_team(request):
    if request.method == "POST":
        form = TeamForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            team_exists = Team.objects.filter(
                team_name=model_instance.team_name).count() > 0
            if team_exists:
                team = Team.objects.filter(
                    team_name=model_instance.team_name).first()
                # model_instance.creation_date = team.creation_date  # todo: is there a better way? sorta hacky
                team.members.add(get_laborer(request))
                team.number_of_members = team.number_of_members + 1
                team.save()

                # todo: improve this
                return HttpResponseRedirect(reverse_lazy('npl:settings'))
            else:
                return render(request, 'npl/team_join.html', {'form': form, 'error': 'Team does not exist!'})

        else:
            return render(request, 'npl/team_form.html', {'form': form, 'error': 'Form is invalid!'})

    else:
        form = TeamForm(request.POST)
        return render(request, 'npl/team_join.html', {'form': form})


def leave_team(request, pk):
    team = Team.objects.filter(id=pk).first()

    laborer = get_laborer(request)
    team.members.remove(laborer)
    team.number_of_members = team.number_of_members - 1
    team.save()
    return HttpResponseRedirect(reverse_lazy('npl:settings'))


def log_in(request):
    return render(request, 'registration/login.html')


def log_out(request):
    auth.logout(request)
    return render(request, 'registration/logged_out.html')


def landing_page(request):
    return render(request, 'registration/about.html')


def features(request):
    return render(request, 'registration/features.html')


def contact(request):
    return render(request, 'registration/contact.html')


class SignUp(generic.CreateView):
    form_class = UserCreationForm  # LaborerCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class CreateUserView(SuccessMessageMixin, generic.CreateView):
    success_url = reverse_lazy('login')
    form_class = CreateUserForm
    template_name = 'registration/signup.html'
    success_message = 'New new user profile has been created'

    def form_valid(self, form):
        c = {'form': form, }
        user = form.save(commit=False)
        # Cleaned(normalized) data
        password = form.cleaned_data['password']
        repeat_password = form.cleaned_data['repeat_password']
        if password != repeat_password:
            messages.error(self.request, "Passwords do not Match",
                           extra_tags='alert alert-danger')
            return render(self.request, self.template_name, c)
        user.set_password(password)
        user.save()

        # Create Laborer
        Laborer.objects.create(user=user, creation_date=timezone.now())

        return super(CreateUserView, self).form_valid(form)


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
    # todo: Change the url to go back to detail view?
