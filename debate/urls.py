from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.debate_list, name='debate_list'),
	url(r'^debate/(?P<pk>[0-9]+)/$', views.debate_list_category, name='debate_list_category'),

    url(r'^debate/agenda/(?P<pk>[0-9]+)/$', views.agenda_detail, name='agenda_detail'),
	url(r'^debate/agenda/offer$', views.offer_agenda, name='offer_agenda'),
    url(r'^debate/agenda/(?P<pk>[0-9]+)/edit/$', views.agenda_edit, name='agenda_edit'),
    
    url(r'^debate/opinion/offer/(?P<agenda_id>[0-9]+)/(?P<stance>\w+)$', views.offer_opinion, name='offer_opinion'),
    url(r'^debate/opinion/(?P<pk>[0-9]+)/edit/$', views.opinion_edit, name='opinion_edit'),
    url(r'^debate/opinion/(?P<pk>[0-9]+)/$', views.opinion_detail, name='opinion_detail'),

    url(r'^debate/arbitration/offer/(?P<parent_id>[0-9]+)$', views.offer_arbitration, name='offer_arbitration'),
	url(r'^debate/arbitration/(?P<pk>[0-9]+)$', views.arbitration_detail, name='arbitration_detail'),

    url(r'^debate/category/$', views.category, name='category'),
]