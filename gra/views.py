import os
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from gra import utils
from django.shortcuts import redirect
@csrf_exempt
def execute_code(request):
    tasks = utils.open_file(os.path.join(settings.BASE_DIR,'gra', 'data', 'zadania.json'))
    level = utils.get_level(request)
    if tasks:
        current_task = tasks[level]
    else:
        current_task = {}
    try:
        if request.method == 'POST':
            if 'clear_button' in request.POST:
                return utils.render_w_cookie(request, { 'title': current_task.get('title', ''), 'content': current_task.get('content', '')},level)
            else:
                code = request.POST['code']
                result = utils.execute_user_code(code)
                return utils.render_w_cookie(request, {'result': result, 'code': code, 'title': current_task.get('title', ''), 'content': current_task.get('content', '')},level)
        else:
            return utils.render_w_cookie(request, { 'title': current_task.get('title', ''), 'content': current_task.get('content', '')},level)
    except Exception:
        return utils.render_w_cookie(request, { 'title': current_task.get('title', ''), 'content': current_task.get('content', '')},level)

@csrf_exempt
def check_answer(request):
    tasks = utils.open_file(os.path.join(settings.BASE_DIR,'gra', 'data', 'zadania.json'))
    answers = utils.open_file(os.path.join(settings.BASE_DIR,'gra', 'data', 'odpowiedzi.json'))
    level = utils.get_level(request) 
    if tasks:
        current_task = tasks[level]
    else:
        current_task = {}
    if answers:
        current_answer = answers[level]
    else:
        current_answer = {}
    if request.method == 'POST': 
        code = request.POST.get('code')
        result = request.POST.get('result')
        if result == current_answer.get('answer',''):
            level += 1
        return utils.redirect_w_cookie(request,'/',{'result': result, 'code': code, 'title': current_task.get('title', ''), 'content': current_task.get('content', '')},level)
    else:
       return redirect('/')
    
def reset_level(request):
   return utils.redirect_w_cookie(request,'/',{},0)