from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^debate/$', views.debate_list, name='debate_list'),

    url(r'^debate/agenda/(?P<pk>[0-9]+)/$', views.agenda_detail, name='agenda_detail'),
	url(r'^debate/agenda/offer$', views.offer_agenda, name='offer_agenda'),
    url(r'^debate/agenda/(?P<pk>[0-9]+)/edit/$', views.agenda_edit, name='agenda_edit'),
    
    url(r'^debate/opinion/offer/(?P<agenda_id>[0-9]+)/(?P<stance>\w+)$', views.offer_opinion, name='offer_opinion'),
    url(r'^debate/opinion/(?P<pk>[0-9]+)/edit/$', views.opinion_edit, name='opinion_edit'),
]