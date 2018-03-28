from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django import forms
from .models import Choice, Question, Encounter
from .forms import EncounterForm
from django.utils import timezone

# Create your views here.


def add_encounter(request):
    if request.method == "POST":
        form = EncounterForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.date_time = timezone.now()
            # todo: how do I make these simply not required?!
            model_instance.lat = 0
            model_instance.lng = 0
            model_instance.save()
            return HttpResponseRedirect(reverse_lazy('npl:encounters'))

    else:
        form = EncounterForm()
        return render(request, 'npl/encounter_form.html', {'form': form})


class EncounterIndex(generic.ListView):
    template_name = 'npl/encounters.html'
    context_object_name = 'encounters_list'

    def get_queryset(self):
        """Return all encounters for this user."""
        return Encounter.objects.order_by('-date_time')


class AddEncounter(generic.edit.CreateView):
    model = Encounter
    fields = ['name', 'action_prayer', 'action_testimony',
              'action_gospel', 'response', 'street_address', 'apt_or_unit', 'city', 'state', 'zip', 'notes']
    success_url = reverse_lazy('npl:encounters')

    def form_valid(self, form):
        form.instance.date_time = timezone.now()
        return super().form_valid(form)


class DetailEncounter(generic.DetailView):
    model = Encounter
    fields = ['name', 'response', 'notes']
    template_name = 'npl/encounter_detail.html'


class DeleteEncounter(generic.DeleteView):
    model = Encounter
    template_name = 'npl/encounter_delete.html'
    success_url = reverse_lazy('npl:encounters')


class EditEncounter(generic.edit.UpdateView):
    model = Encounter
    fields = ['name', 'action_prayer', 'action_testimony',
              'action_gospel', 'response', 'street_address', 'apt_or_unit', 'city', 'state', 'zip', 'notes']
    success_url = reverse_lazy('npl:encounters')
    #todo: Change the url to go back to detail view?


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'npl/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('npl:results', args=(question.id,)))
