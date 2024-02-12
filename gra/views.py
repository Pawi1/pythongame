import os
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from gra import utils
from django.shortcuts import redirect
from gra import crypto
from django.shortcuts import render
@csrf_exempt
def main(request):
    if request.method == 'POST':
        if 'execute' in request.POST:
            return execute_code(request)
        else:
            return check_answer(request)
    else:
        return first_entry(request)

@csrf_exempt
def execute_code(request):
    tasks = utils.open_file(os.path.join(settings.BASE_DIR,'gra', 'data', 'zadania.json'))
    level = utils.get_level(request)
    task = tasks[level]
    try:
        if request.method == 'POST':
            if 'clear_button' in request.POST:
                return utils.render_w_cookie(request, { 'title': task.get('title', ''), 'content': task.get('content', '')},level)
            else: 
                code = request.POST['code']
                result = utils.execute_user_code(code)
                return utils.render_w_cookie(request, {'result': result, 'code': code, 'title': task.get('title', ''), 'content': task.get('content', '')},level)
        else:
            return utils.render_w_cookie(request, { 'title': task.get('title', ''), 'content': task.get('content', '')},level)
    except Exception:
        return utils.render_w_cookie(request, { 'title': task.get('title', ''), 'content': task.get('content', '')},level)

@csrf_exempt
def check_answer(request):
    tasks = utils.open_file(os.path.join(settings.BASE_DIR,'gra', 'data', 'zadania.json'))
    answers = utils.open_file(os.path.join(settings.BASE_DIR,'gra', 'data', 'odpowiedzi.json'))
    level = utils.get_level(request) 
    task = tasks[level]
    answer = answers[level]
    if request.method == 'POST': 
        if int(crypto.decrypt_data(request.POST['cookie'])) == level:
            code = request.POST.get('code')
            result = request.POST.get('result')
            print(list(result))
            print(list(answer.get('answer','')))
            if result == answer.get('answer',''):
                level += 1
                task = tasks[level]
                return utils.render_w_cookie(request, {'answer': 'True', 'title': task.get('title', ''), 'content': task.get('content', '')},level)
            return utils.render_w_cookie(request, {'answer': 'False','result': result, 'code': code, 'title': task.get('title', ''), 'content': task.get('content', '')},level)
        else:
          return redirect('/')
    else:
        return redirect('/')

def first_entry(request):
    level = utils.get_level(request)
    if level > 0:
        if 'continue' in request.GET:
            if request.GET['continue'] == 'True':
                tasks = utils.open_file(os.path.join(settings.BASE_DIR,'gra', 'data', 'zadania.json'))
                task = tasks[level]
                return utils.render_w_cookie(request, { 'title': task.get('title', ''), 'content': task.get('content', '')},level)
            else:
                return reset_level(request)
        else:  
            return render(request,'main.html',{'continue' : True})
    else:
        #!TODO INTRO
        tasks = utils.open_file(os.path.join(settings.BASE_DIR,'gra', 'data', 'zadania.json'))
        task = tasks[level]
        return utils.render_w_cookie(request, { 'title': task.get('title', ''), 'content': task.get('content', '')},level)

def reset_level(request):
   return utils.redirect_w_cookie(request,'/',0)

# ONLY ON DEBUG !!
def next_level(request):
   return utils.redirect_w_cookie(request,'/?debug&continue=True',utils.get_level(request)+1)
def previous_level(request):
   return utils.redirect_w_cookie(request,'/?debug&continue=True',utils.get_level(request)-1)