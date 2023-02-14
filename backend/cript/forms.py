from django.forms import ModelForm
from cript.models import Message
from django.forms import ModelForm, TextInput, Textarea, Select


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['original_message', 'key', 'method']
        widgets = {
            'original_message': Textarea(attrs={
                'class': "form-control",
                'style': 'max-width: 200px;',
                'placeholder': 'Message'
            }),
            'key': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 200px;',
                'placeholder': 'Key'
            }),
            'method': Select(attrs={
                'class': "btn btn-warning w-100 text-center rounded"
            })
        }
