from django.shortcuts import render
import os
import json
from django.conf import settings
from .forms import CommandForm
from django.views.decorators.csrf import csrf_exempt
from .utils import execute_user_code
from gra import crypto
from django.http import HttpResponse

@csrf_exempt
def execute_code(request):
    tasks = open_file(os.path.join(settings.BASE_DIR,'gra', 'data', 'zadania.json'))
    level = get_level(request)
    if tasks:
        current_task = tasks[level]
    else:
        current_task = {}
    try:
        if request.method == 'POST':
            form = CommandForm(request.POST)
            if 'clear_button' in request.POST:
                return cookie(render(request, 'main.html', {'form': form, 'title': current_task.get('title', ''), 'content': current_task.get('content', '')}),level)
            elif form.is_valid():
                command = form.cleaned_data['command']
                result = execute_user_code(command)
                return cookie(render(request, 'main.html', {'result': result, 'command': command, 'title': current_task.get('title', ''), 'content': current_task.get('content', '')}),level)
        else:
            form = CommandForm()
        return cookie(render(request, 'main.html', {'form': form, 'title': current_task.get('title', ''), 'content': current_task.get('content', '')}),level)
    except Exception as e:
        return cookie(render(request, 'main.html', {'form': form, 'title': current_task.get('title', ''), 'content': current_task.get('content', '')}),level)

@csrf_exempt
def check_answer(request):
    tasks = open_file(os.path.join(settings.BASE_DIR,'gra', 'data', 'zadania.json'))
    answers = open_file(os.path.join(settings.BASE_DIR,'gra', 'data', 'odpowiedzi.json'))
    level = get_level(request)
    
    if tasks:
        current_task = tasks[level]
    else:
        current_task = {}
    if answers:
        current_answer = answers[level]
    else:
        current_answer = {}
    
    
def open_file(file_path):    
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
    return data

def cookie(r,level):
    response = HttpResponse(r)
    response.set_cookie('level', crypto.encrypt_data(level), max_age=2629440)
    return response

def get_level(request):
    level_cookie = request.COOKIES.get('level')
    if level_cookie:
        level = crypto.decrypt_data(level_cookie)
    else:
        level = 0
    return level