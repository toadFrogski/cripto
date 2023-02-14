from django.views.generic import View
from django.shortcuts import render, redirect
from cript.forms import MessageForm
from cript.models import Message
from cript.services import ConvertADFGX


class EncodeView(View):

    def get(self, request):
        messages = Message.objects.filter(type=Message.Types.ENCODE)
        return render(request, 'encode.html', {
            'form': MessageForm(),
            'messages': messages
        })

    def post(self, request):
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.type = 'EN'
            if message.method == 'GX':
                message.encoded_message = ConvertADFGX.convert_to_ADFGX(
                    message.original_message, message.key)
            elif message.method == 'VX':
                message.encoded_message = ConvertADFGX.convert_to_ADFGVX(
                    message.original_message, message.key)
            message.save()
            form.save_m2m()
        return redirect(to="encode")


class DecodeView(View):

    def get(self, request):
        messages = Message.objects.filter(type=Message.Types.DECODE)
        return render(request, 'decode.html', {
            'form': MessageForm(),
            'messages': messages
        })

    def post(self, request):
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.type = 'DE'
            if message.method == 'GX':
                message.encoded_message = ConvertADFGX.convert_from_ADFG_X(
                    message.original_message, message.key, options={'replace': ['j', 'i']})
            elif message.method == 'VX':
                message.encoded_message = ConvertADFGX.convert_from_ADFG_X(
                    message.original_message, message.key, 'adfgvx', 'abcdefghijklmnopqrstuvwxyz0123456789')
            message.save()
            form.save_m2m()
        return redirect(to="decode")

