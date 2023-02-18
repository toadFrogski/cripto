from django.forms import ModelForm
from cript.models import ADFGX, Playfair
from django.forms import ModelForm, TextInput, Textarea, Select


class ADFGXForm(ModelForm):
    class Meta:
        model = ADFGX
        fields = ['original_message', 'key', 'method']
        widgets = {
            'original_message': Textarea(attrs={
                'class': "form-control",
                'style': 'max-width: 200px;',
                'placeholder': 'ADFGX'
            }),
            'key': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 200px;',
                'placeholder': 'Key'
            }),
            'method': Select(attrs={
                'class': "btn btn-warning w-100 text-center rounded"
                }
            )
        }


class PlayfairForm(ModelForm):
    class Meta:
        model = Playfair
        fields = ['original_message', 'key']
        widgets = {
            'original_message': Textarea(attrs={
                'class': "form-control",
                'style': 'max-width: 200px;',
                'placeholder': 'ADFGX'
            }),
            'key': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 200px;',
                'placeholder': 'Key'
            }),
        }
