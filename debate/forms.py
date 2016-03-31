from django import forms

from .models import Agenda, Opinion
from django.utils.html import strip_tags

class AgendaForm(forms.ModelForm):

    class Meta:
        model = Agenda
        fields = ('text', 'parent_agenda', 'depth', 'category')
        widgets = {'parent_agenda': forms.HiddenInput()
        			,'depth':forms.HiddenInput()}

class OpinionForm(forms.ModelForm):

    class Meta:
        model = Opinion
        fields = ('agenda', 'stance','text',)
        widgets = {'agenda':forms.HiddenInput()
        			,'stance': forms.HiddenInput()}

    def clean(self):
        # To keep the main validation and error messages
        super(OpinionForm, self).clean()

        # Now it's time to add your custom validation
        length = len(strip_tags(self.cleaned_data['text']))
        if length < 100 :
            #self._errors['text']='your text length is too short'
            # you may also use the below line to custom your error message, but it doesn't work with me for some reason
            raise forms.ValidationError('100글자 이상으로 논리적인 글을 써주세요.( '+str(length)+' 글자)')
