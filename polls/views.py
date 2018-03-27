from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from .models import Choice, Question, Encounter
from django.utils import timezone

# Create your views here.


class EncounterIndex(generic.ListView):
    template_name = 'polls/encounters.html'
    context_object_name = 'encounters_list'

    def get_queryset(self):
        """Return all encounters for this user."""
        return Encounter.objects.order_by('-date_time')


class AddEncounter(generic.edit.CreateView):
    model = Encounter
    fields = ['name', 'action_prayer', 'action_testimony',
              'action_gospel', 'response', 'notes']
    success_url = reverse_lazy('polls:encounters')

    def form_valid(self, form):
        form.instance.date_time = timezone.now()
        return super().form_valid(form)


class DetailEncounter(generic.DetailView):
    model = Encounter
    fields = ['name', 'response', 'notes']
    template_name = 'polls/encounter_detail.html'


class DeleteEncounter(generic.DeleteView):
    model = Encounter
    template_name = 'polls/encounter_delete.html'
    success_url = reverse_lazy('polls:encounters')


class EditEncounter(generic.edit.UpdateView):
    model = Encounter
    fields = ['name', 'action_prayer', 'action_testimony',
              'action_gospel', 'date_time', 'response', 'notes']
    success_url = reverse_lazy('polls:encounters')
    #todo: Change the url to go back to detail view?


class EditView(generic.edit.UpdateView):
    model = Question
    fields = ['question_text']
    success_url = reverse_lazy('polls:index')


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
