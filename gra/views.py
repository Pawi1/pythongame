from django.shortcuts import render
import os
import json
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .utils import execute_user_code
from gra import crypto
from django.shortcuts import redirect
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
            if 'clear_button' in request.POST:
                return render_w_cookie(request, { 'title': current_task.get('title', ''), 'content': current_task.get('content', '')},level)
            else:
                code = request.POST['code']
                result = execute_user_code(code)
                return render_w_cookie(request, {'result': result, 'code': code, 'title': current_task.get('title', ''), 'content': current_task.get('content', '')},level)
        else:
            return render_w_cookie(request, { 'title': current_task.get('title', ''), 'content': current_task.get('content', '')},level)
    except Exception as e:
        return render_w_cookie(request, { 'title': current_task.get('title', ''), 'content': current_task.get('content', '')},level)

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
    if request.method == 'POST': 
        level += 1
        code = request.POST['code']
        result = request.POST['result']
        return redirect_w_cookie(request,'/',{'result': result, 'code': code, 'title': current_task.get('title', ''), 'content': current_task.get('content', '')},level)
    else:
       return redirect('/')
    
def open_file(file_path):    
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
    return data

def redirect_w_cookie(r,p,c,l):
    rdct = redirect(p,c)
    if r.COOKIES.get('level'):
        rdct.delete_cookie('level')
        rdct.delete_cookie('d_level')
    rdct.set_cookie('level', crypto.encrypt_data(l), max_age=2629440)
    rdct.set_cookie('d_level', l, max_age=2629440)
    return rdct

def render_w_cookie(r,c,l):
    rndr = render(r,'main.html',c)
    if r.COOKIES.get('level'):
        rndr.delete_cookie('level')
        rndr.delete_cookie('d_level')
    rndr.set_cookie('level', crypto.encrypt_data(l), max_age=2629440)
    rndr.set_cookie('d_level', l, max_age=2629440)
    return rndr

def get_level(request):
    if not request.COOKIES.get('level'):
        return 0
    level = crypto.decrypt_data(request.COOKIES.get('level'))
    return int(level)