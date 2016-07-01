from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template
from django.template import RequestContext
from django.utils import timezone
from debate.models import Agenda, Opinion, Category, OpinionLink
from .forms import AgendaForm, OpinionForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.urlresolvers import reverse

import logging
logger = logging.getLogger(__name__)

default_text = "예의있고 논리적인 글로 올바른 토론문화를 만듭시다."

def debate_list(request):
    request.session.set_expiry(0)
    agendas = Agenda.objects.filter(depth=0).order_by('created_date')
    return render(request, 'debate/debate_list.html', {'agendas': agendas})

def debate_list_category(request, pk):
    request.session.set_expiry(0)
    agendas = Agenda.objects.filter(category=pk).filter(depth=0).order_by('created_date')
    return render(request, 'debate/debate_list.html', {'agendas': agendas})

def agenda_detail(request, pk):
    request.session.set_expiry(0)
    agenda = get_object_or_404(Agenda, pk=pk)
    agree = agenda.opinion_set.filter(stance=10)
    disagree = agenda.opinion_set.filter(stance=90)
    arbitrations = Agenda.objects.filter(parent_agenda=pk)
    return render(request, 'debate/agenda_detail.html',
                         {'agenda': agenda, 'agree':agree,
                            'disagree':disagree, 'arbitrations':arbitrations})

def category(request):
    category = Category.objects.all().order_by('name')
    template = get_template('debate/category.html')
#    value = RequestContext(request, {'category':category})
#    output = template.render(value)
    output = template.render({'category':category}, request)
    return HttpResponse(output)

@login_required
def offer_agenda(request):
    request.session.set_expiry(0)
    if request.method == "POST":
        form = AgendaForm(request.POST)
        if form.is_valid():
            agenda = form.save(commit=False)
            agenda.author = request.user
            agenda.save()
            return redirect('debate.views.agenda_detail', pk=agenda.pk)
    else:
        form = AgendaForm(initial={"text":default_text})
    return render(request, 'debate/agenda_edit.html', {'form': form})

@login_required
def agenda_edit(request, pk):
    request.session.set_expiry(0)
    
    agenda = get_object_or_404(Agenda, pk=pk)
    parent_agenda = agenda.parent_agenda
    if request.method == "POST":
        form = AgendaForm(request.POST, instance=agenda)
        if form.is_valid():
            agenda = form.save(commit=False)
            agenda.author = request.user
            agenda.modified_date = timezone.now()
            agenda.save()
            if agenda.depth == 0:
                return redirect('debate.views.agenda_detail', pk=agenda.pk)
            else :
                return redirect('debate.views.arbitration_detail', pk=agenda.pk)
    else:
        if not request.user == agenda.author:
            return redirect(reverse('agenda_detail', args=(pk,)))
        if agenda.depth > 0:
            parent_agenda = agenda.parent_agenda
        
        form = AgendaForm(instance=agenda)
        
        
    return render(request, 'debate/agenda_edit.html', {'form': form})







@login_required
def offer_opinion(request, agenda_id, stance):
    request.session.set_expiry(0)
    agenda = get_object_or_404(Agenda, pk=agenda_id)
    if request.method == "POST":
        form = OpinionForm(request.POST)
        if form.is_valid():
            opinion = form.save(commit=False)
            opinion.author = request.user
            opinion.save()
            return redirect('debate.views.agenda_detail', pk=opinion.agenda.pk)
    else:
        form = OpinionForm(initial={'stance':int(stance), "agenda":agenda, "text":default_text})

    return render(request, 'debate/opinion_edit.html', {'form': form, "agenda":agenda})

@login_required
def opinion_edit(request, pk):
    request.session.set_expiry(0)
    opinion = get_object_or_404(Opinion, pk=pk)
    if request.method == "POST":
        form = OpinionForm(request.POST, instance=opinion)
        if form.is_valid():
            opinion = form.save(commit=False)
            opinion.author = request.user
            opinion.modified_date = timezone.now()
            opinion.save()
            return redirect('debate.views.agenda_detail', pk=opinion.agenda.pk)
        else :
            logger.debug("form error %s", form.errors)
    else:
        form = OpinionForm(instance=opinion)
    return render(request, 'debate/opinion_edit.html', {'form': form, 'agenda':opinion.agenda})

def opinion_detail(request, pk):
    request.session.set_expiry(0)
    opinion = get_object_or_404(Opinion, pk=pk)
    opinionLinks = OpinionLink.objects.filter(parent_opinion=pk)

    

    return render(request, 'debate/opinion_detail.html',
                         {'agenda': opinion.agenda, 'opinion':opinion,
                            'opinionLinks':opinionLinks})








@login_required
def offer_arbitration(request, parent_id):
    request.session.set_expiry(0)
    if request.method == "POST":
        form = AgendaForm(request.POST)
        if int(form['depth'].value()) > 3 :
            return redirect(reverse('debate_list'))
        if form.is_valid():
            agenda = form.save(commit=False)
            agenda.author = request.user
            agenda.save()
            return redirect('debate.views.arbitration_detail', pk=agenda.pk)
    else:
        agenda = get_object_or_404(Agenda, pk=parent_id)
        form = AgendaForm(initial={'parent_agenda':parent_id, 
                                    'depth':agenda.depth+1, 
                                    'category':agenda.category,
									"text":default_text})
    return render(request, 'debate/agenda_edit.html', {'form': form})


def arbitration_detail(request, pk):
    #중재안 본글 상세 조회
    request.session.set_expiry(0)
    agenda = get_object_or_404(Agenda, pk=pk)
    agree = agenda.opinion_set.filter(stance=10)
    disagree = agenda.opinion_set.filter(stance=90)
    arbitrations = Agenda.objects.filter(parent_agenda=pk)

    parents = ()
    parent_pk = 0

    #한단계 상위 글
    parent = agenda.parent_agenda
    logger.debug("first %s", parent)
    parents = (parent, )
    
    #두단계 상위 글
    if not parent.parent_agenda == None :     
        parent = parent.parent_agenda
        logger.debug("second %s", parent)
        parents = (parent, ) + parents
    
    #세단계 상위 글
    if not parent.parent_agenda == None :     
        parent = parent.parent_agenda
        logger.debug("third %s", parent)
        parents = (parent, ) + parents
    
    logger.debug(parents)

    """
    parent = get_object_or_404(Agenda, pk=parent_pk)
    logger.debug("second %s",parent)
    parents = parents + (parent, )
    if not parent.parent_agenda == None :                
        parent_pk = parent.parent_agenda.pk

    parent = get_object_or_404(Agenda, pk=parent_pk)
    parents = parents + (parent, )
    logger.debug("third %s",parent)


    logger.debug(parents)

    while parent_pk :
        parent = get_object_or_404(Agenda, pk=4)
        if parent == None :
            break
        else :
            parents = parents + (parent,)
            parent_pk = parent.parent_agenda
    """
    return render(request, 'debate/agenda_detail.html',
                         {'agenda': agenda, 'agree':agree,
                            'disagree':disagree, 'arbitrations':arbitrations, 'parents':parents})
