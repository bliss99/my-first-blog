from django import forms

from .models import Agenda, Opinion

class AgendaForm(forms.ModelForm):

    class Meta:
        model = Agenda
        fields = ('text',)

class OpinionForm(forms.ModelForm):

    class Meta:
        model = Opinion
        fields = ('agenda', 'stance','text',)
