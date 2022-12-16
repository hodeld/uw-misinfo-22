from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from django import forms
from misinfo_main.models import Paper_SeSc, DBQuery


class PaperFilterForm(forms.ModelForm):
    #paperclass = EventTypeChoiceField(queryset=EventType.objects.all())
    pk = forms.IntegerField(required=False, )
    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.id:
            self.fields['pk'].initial = self.instance.id
            self.fields['pk'].widget = forms.HiddenInput()
            #self.fields['pk'].initial = self.instance.id
        self.fields['corpusid'].widget.attrs['readonly'] = True
        self.helper = FormHelper(self)
        self.helper.layout.append(


            #Field('pk', type='hidden'),
            Submit('submitform', 'Save', css_class='btn btn-primary',
                   css_id='id_savepaper'),

        )


    class Meta:
        model = Paper_SeSc
        exclude = ['dbquery', 'title', 'abstract', 'url_sesc', 'pk']
        widgets = {
            #'comment': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
            #'pk': forms.HiddenInput()
        }


class DBQueryAdminForm(forms.ModelForm):
  class Meta:
    model = DBQuery
    widgets = {
      'query': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
    }
    fields = '__all__'