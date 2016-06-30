from django import forms

from .models import Agenda, Opinion
from django.utils.html import strip_tags

class AgendaForm(forms.ModelForm):
    
    class Meta:
        model = Agenda
        fields = ('category', 'text', 'parent_agenda', 'depth')
        widgets = {'parent_agenda': forms.HiddenInput(),'depth':forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super(AgendaForm, self).__init__(*args, **kwargs)
        self.fields['category'].error_messages = {'required': '카테고리를 선택하세요'}

    def clean(self):
        # To keep the main validation and error messages
        cleaned_data = super(AgendaForm, self).clean()
        text = cleaned_data.get("text")
        
        # Now it's time to add your custom validation
        length = 0
        if text :
           length = len(strip_tags(self.cleaned_data['text']))
        if length < 200 :
            self._errors['text']='200글자 이상으로 논리적인 글을 써주세요.( '+str(length)+'글자는 의견을 표현하기에 충분하지 않을 수 있습니다.)'
            # you may also use the below line to custom your error message, but it doesn't work with me for some reason
            #raise forms.ValidationError('200글자 이상으로 논리적인 글을 써주세요.( '+str(length)+'글자는 의견을 표현하기에 충분하지 않을 수 있습니다.)')


class OpinionForm(forms.ModelForm):

    class Meta:
        model = Opinion
        fields = ('agenda', 'stance','text',)
        widgets = {'agenda':forms.HiddenInput(),'stance': forms.HiddenInput()}

    def clean(self):
        # To keep the main validation and error messages
        cleaned_data = super(OpinionForm, self).clean()
        text = cleaned_data.get("text")
        
        # Now it's time to add your custom validation
        length = 0
        if text :
           length = len(strip_tags(self.cleaned_data['text']))
        if length < 200 :
            self._errors['text']='200글자 이상으로 논리적인 글을 써주세요.( '+str(length)+'글자는 의견을 표현하기에 충분하지 않을 수 있습니다.)'
            # you may also use the below line to custom your error message, but it doesn't work with me for some reason
            #raise forms.ValidationError('200글자 이상으로 논리적인 글을 써주세요.( '+str(length)+'글자는 의견을 표현하기에 충분하지 않을 수 있습니다.)')
