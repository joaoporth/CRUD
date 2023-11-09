import sys, os

from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.contrib import messages
from django.utils import timezone

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from unidecode import unidecode
import json


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from . import models


import logging


from time import sleep
import requests

# LOGGER
class _Logger:
    logging.basicConfig(
        level=logging.INFO,  # Set the logging level (e.g., INFO, DEBUG)
        format='%(asctime)s [%(levelname)s] %(message)s',  # Define log message format
        datefmt='%Y-%m-%d %H:%M:%S'  # Define the date format
    )

    logger = logging.getLogger("app")

    log_file = "response.log"  # Specify the file path
    file_handler = logging.FileHandler(log_file)

    file_format = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(file_format)

    logger.addHandler(file_handler)

def json_response(data:dict, response:dict, status=400) -> JsonResponse:
    _Logger.logger.info(f"DATA: {data}")

    if status == 200:
        _Logger.logger.info(f"RESPONSE {status}: {response}")
    else:
        _Logger.logger.error(f"RESPONSE {status}: {response}")

    return JsonResponse(response, json_dumps_params={'ensure_ascii': False, 'indent': 4}, content_type='application/json', status = status)


class Dash:
    class Index(View):
        template_name = 'index.html'

        def get(self, *args, **kwargs):
            context = {}

            return render(self.request, self.template_name, context=context)


    class Login(View):
        template_name = 'login.html'

        def get(self, *args, **kwargs):
            context = {}

            return render(self.request, self.template_name, context=context)

        def post(self, *args, **kwargs):

            data:dict = json.loads(self.request.body.decode())

            username = data.get('username')
            password = data.get('password')

            if not username:
                return json_response(data, {"error": 'O Login está vazio'},401)

            if not password:
                return json_response(data, {"error": 'A Senha está vazia'},401)


            auth = authenticate(username=username, password=password)

            if auth:
                user_account = User.objects.filter(username=username).first()

                login(self.request, user_account)

                return json_response(data, {"success": 'Autenticado'},200)


            return json_response(data, {"error": 'login ou Senha incorreto'},401)



    class Cadastro(View):
        template_name = 'cadastro.html'

        def get(self, *args, **kwargs):
            context = {}

            return render(self.request, self.template_name, context=context)

        def post(self, *args, **kwargs):

            data:dict = json.loads(self.request.body.decode())

            full_name = data.get('full_name')
            email = data.get('email')
            password = data.get('password')
            confirmPassword = data.get('confirmPassword')


            if not full_name:
                return json_response(data, {"error": 'O Nome está vazio'},401)


            try:
                nome, sobrenome = full_name.split(' ')

                sobrenome = sobrenome.strip()

                if not sobrenome:
                    return json_response(data, {"error": 'Digite seu sobrenome'},401)

                if len(full_name) <6:
                    raise

            except:
                return json_response(data, {"error": 'Digite seu nome e sobrenome'},401)


            if not email:
                return json_response(data, {"error": 'O Email está vazio'},401)

            if not '@' in email and not '.' in email:
                return json_response(data, {"error": 'Email inválido'},401)

            if User.objects.filter(username=email):
                return json_response(data, {"error": 'Já existe um usuário cadastrado com este Email'},401)


            if not password:
                return json_response(data, {"error": 'A Senha esta vazia'},401)

            if len(password) <6:
                return json_response(data, {"error": 'A Senha precisa ter 6 digitos'},401)


            if password != confirmPassword:
                return json_response(data, {"error": 'As Senhas precisam ser iguais'},401)


            # crie o cadastro no banco de dados

            return json_response(data, {"success": 'Usuário cadastrado'},200)


    class _LogOut(View):
        template_name = 'index.html'

        def get(self, *args, **kwargs):
            logout(self.request)
            context = {}

            return render(self.request, self.template_name, context=context)
