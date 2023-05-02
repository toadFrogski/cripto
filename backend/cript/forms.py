from django.forms import ModelForm
from cript.models import ADFGX, Playfair, Salsa, Des, Sha
from django.forms import ModelForm, TextInput, Textarea, Select


class ADFGXForm(ModelForm):
    class Meta:
        model = ADFGX
        fields = ['original_message', 'key', 'method']
        widgets = {
            'original_message': Textarea(attrs={
                'class': "form-control",
                'placeholder': 'ADFGX'
            }),
            'key': TextInput(attrs={
                'class': "form-control",
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
                'placeholder': 'ADFGX'
            }),
            'key': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Key'
            }),
        }


class SalsaForm(ModelForm):
    class Meta:
        model = Salsa
        fields = ['original_message', 'key']
        widgets = {
            'original_message': Textarea(attrs={
                'class': "form-control",
                'placeholder': 'Salsa'
            }),
            'key': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Key'
            }),
        }


class DesForm(ModelForm):
    class Meta:
        model = Des
        fields = ['original_message', 'key']
        widgets = {
            'original_message': Textarea(attrs={
                'class': "form-control",
                'placeholder': 'Des'
            }),
            'key': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Key',
            }),
        }


class ShaForm(ModelForm):
    class Meta:
        model = Sha
        fields = ['original_message']
        widgets = {
            'original_message': Textarea(attrs={
                'class': "form-control",
                'placeholder': 'Sha256'
            })
        }
