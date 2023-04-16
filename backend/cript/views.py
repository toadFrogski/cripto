import hashlib
import json
from django.views.generic import View
from django.shortcuts import render, redirect
from cript.forms import ADFGXForm, PlayfairForm, SalsaForm, DesForm
from cript.models import ADFGX, Playfair, Salsa as SalsaModel, Des as DesModel
from cript.services.Salsa import Salsa
from cript.services.ConvertPlaydair import ConvertPlayfair
from cript.services.ConvertADFGX import ConvertADFGX
from cript.services.Des import Des


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


class SalsaEncodeView(View):

    def get(self, request):
        messages = SalsaModel.objects.filter(type=SalsaModel.Types.ENCODE)
        return render(request, 'page.html', {
            'form': SalsaForm(),
            'messages': messages,
            'type': 'Encode',
            'color': 'bg-success'
        })

    def post(self, request):
        form = SalsaForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.type = 'EN'
            message.encoded_message = SalsaEncodeView.crypt(
                message.original_message, message.key)
            message.save()
            form.save_m2m()
        return redirect(to="salsa_encode")

    def crypt(message, key):
        message = message.encode("UTF-8")
        k32 = hashlib.sha256(key.encode("UTF-8")).digest()
        salsa = Salsa()
        streamkey = salsa(k32, [3, 1, 4, 1, 5, 9, 2, 6], [
                          7, 0, 0, 0, 0, 0, 0, 0])
        return "|".join([str(m ^ streamkey[i % 16] & salsa._mask) for i, m in enumerate(message)])


class SalsaDecodeView(View):

    def get(self, request):
        messages = SalsaModel.objects.filter(type=SalsaModel.Types.DECODE)
        return render(request, 'page.html', {
            'form': SalsaForm(),
            'messages': messages,
            'type': 'Decode',
            'color': 'bg-success'
        })

    def post(self, request):
        form = SalsaForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.type = 'DE'
            message.encoded_message = SalsaDecodeView.crypt(
                message.original_message, message.key)
            message.save()
            form.save_m2m()
        return redirect(to="salsa_decode")

    def crypt(message, key):
        message = [int(char) for char in message.split("|")]
        k32 = hashlib.sha256(key.encode("UTF-8")).digest()
        salsa = Salsa()
        streamkey = salsa(k32, [3, 1, 4, 1, 5, 9, 2, 6], [
                          7, 0, 0, 0, 0, 0, 0, 0])
        return "".join([chr(m ^ streamkey[i % 16] & salsa._mask).encode("UTF-8").decode("UTF-8") for i, m in enumerate(message)])

class DesEncodeView(View):

    def get(self, request):
        messages = DesModel.objects.filter(type=DesModel.Types.ENCODE)
        return render(request, 'page.html', {
            'form': DesForm(),
            'messages': messages,
            'type': 'Encode',
            'color': 'bg-secondary'
        })

    def post(self, request):
        form = DesForm(request.POST)
        if form.is_valid():
            d = Des()
            message = form.save(commit=False)
            message.type = 'EN'
            message.encoded_message = d.encrypt(
                message.key, message.original_message)
            message.save()
            form.save_m2m()
        return redirect(to="des_encode")


class DesDecodeView(View):

    def get(self, request):
        messages = DesModel.objects.filter(type=DesModel.Types.DECODE)
        return render(request, 'page.html', {
            'form': DesForm(),
            'messages': messages,
            'type': 'Decode',
            'color': 'bg-secondary'
        })

    def post(self, request):
        form = DesForm(request.POST)
        if form.is_valid():
            d = Des()
            message = form.save(commit=False)
            message.type = 'DE'
            message.encoded_message = d.decrypt(
                message.key, message.original_message)
            message.save()
            form.save_m2m()
        return redirect(to="des_decode")
