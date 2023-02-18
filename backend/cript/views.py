import json
from django.views.generic import View
from django.shortcuts import render, redirect
from cript.forms import ADFGXForm, PlayfairForm
from cript.models import ADFGX, Playfair
from cript.services import ConvertADFGX, ConvertPlayfair

class ADFGXEncodeView(View):

    def get(self, request):
        messages = ADFGX.objects.filter(type=ADFGX.Types.ENCODE)
        return render(request, 'page.html', {
            'form': ADFGXForm(),
            'messages': messages,
            'type': 'Encode',
            'color': 'bg-warning'
        })

    def post(self, request):
        form = ADFGXForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.type = 'EN'
            if message.method == 'ADFGX':
                message.encoded_message = ConvertADFGX.convert_to_ADFGX(
                    message.original_message, message.key)
            elif message.method == 'ADFGVX':
                message.encoded_message = ConvertADFGX.convert_to_ADFGVX(
                    message.original_message, message.key)
            message.save()
            form.save_m2m()
        return redirect(to="adfgx_encode")


class ADFGXDecodeView(View):

    def get(self, request):
        messages = ADFGX.objects.filter(type=ADFGX.Types.DECODE)
        return render(request, 'page.html', {
            'form': ADFGXForm(),
            'messages': messages,
            'type': 'Decode',
            'color': 'bg-warning'
        })

    def post(self, request):
        form = ADFGXForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.type = 'DE'
            if message.method == 'ADFGX':
                message.encoded_message = ConvertADFGX.convert_from_ADFG_X(
                    message.original_message, message.key, options={'replace': ['j', 'i']})
            elif message.method == 'ADFGVX':
                message.encoded_message = ConvertADFGX.convert_from_ADFG_X(
                    message.original_message, message.key, 'adfgvx', 'abcdefghijklmnopqrstuvwxyz0123456789')
            message.save()
            form.save_m2m()
        return redirect(to="adfgx_decode")

class PlayfairEncodeView(View):

    def get(self, request):
        messages = Playfair.objects.filter(type=Playfair.Types.ENCODE)
        return render(request, 'page.html', {
            'form': PlayfairForm(),
            'messages': messages,
            'type': 'Encode',
            'color': 'bg-info'
        })

    def post(self, request):
        form = PlayfairForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.type = 'EN'
            message.encoded_message = ConvertPlayfair.convert_to_playfair(
                message.original_message, message.key)
            message.save()
            form.save_m2m()
        return redirect(to="playfair_encode")

class PlayfairDecodeView(View):

    def get(self, request):
        messages = Playfair.objects.filter(type=Playfair.Types.DECODE)
        return render(request, 'page.html', {
            'form': PlayfairForm(),
            'messages': messages,
            'type': 'Decode',
            'color': 'bg-info'
        })

    def post(self, request):
        form = PlayfairForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.type = 'DE'
            message.encoded_message = ConvertPlayfair.convert_from_playfair(
                message.original_message, message.key)
            message.save()
            form.save_m2m()
        return redirect(to="playfair_decode")