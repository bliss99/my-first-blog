from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from debate.models import Agenda, Opinion
from .forms import AgendaForm, OpinionForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

import logging
logger = logging.getLogger(__name__)

def debate_list(request):
    agendas = Agenda.objects.all().order_by('created_date')
    return render(request, 'debate/debate_list.html', {'agendas': agendas})

def agenda_detail(request, pk):
    agenda = get_object_or_404(Agenda, pk=pk)
    agree = agenda.opinion_set.filter(stance=10)
    disagree = agenda.opinion_set.filter(stance=90)
    return render(request, 'debate/agenda_detail.html', {'agenda': agenda, 'agree':agree, 'disagree':disagree})

@login_required
def offer_agenda(request):
    if request.method == "POST":
        form = AgendaForm(request.POST)
        if form.is_valid():
            agenda = form.save(commit=False)
            agenda.author = request.user
            agenda.save()
            return redirect('debate.views.agenda_detail', pk=agenda.pk)
    else:
        form = AgendaForm()
    return render(request, 'debate/agenda_edit.html', {'form': form})

@login_required
def agenda_edit(request, pk):
    agenda = get_object_or_404(Agenda, pk=pk)
    if request.method == "POST":
        form = AgendaForm(request.POST, instance=agenda)
        if form.is_valid():
            agenda = form.save(commit=False)
            agenda.author = request.user
            agenda.modified_date = timezone.now()
            agenda.save()
            return redirect('debate.views.agenda_detail', pk=agenda.pk)
    else:
        form = AgendaForm(instance=agenda)
    return render(request, 'debate/agenda_edit.html', {'form': form})

@login_required
def offer_opinion(request, agenda_id, stance):
    if request.method == "POST":
        form = OpinionForm(request.POST)
        if form.is_valid():
            opinion = form.save(commit=False)
            opinion.author = request.user
            opinion.save()
            return redirect('debate.views.agenda_detail', pk=opinion.agenda.pk)
    else:
        agenda = get_object_or_404(Agenda, pk=agenda_id)
        form = OpinionForm(initial={'stance':stance, "agenda":agenda})

    return render(request, 'debate/opinion_edit.html', {'form': form})

@login_required
def opinion_edit(request, pk):
    opinion = get_object_or_404(Opinion, pk=pk)
    if request.method == "POST":
        form = OpinionForm(request.POST, instance=opinion)
        if form.is_valid():
            opinion = form.save(commit=False)
            opinion.author = request.user
            opinion.modified_date = timezone.now()
            opinion.save()
            return redirect('debate.views.agenda_detail', pk=opinion.pk)
    else:
        form = OpinionForm(instance=opinion)
    return render(request, 'debate/agenda_edit.html', {'form': form})

