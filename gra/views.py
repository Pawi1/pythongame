from django.shortcuts import render
import os
import json
from django.conf import settings
from .forms import CommandForm
from django.views.decorators.csrf import csrf_exempt
from .utils import execute_user_code

@csrf_exempt
def execute_command(request):
    file_path = os.path.join(settings.BASE_DIR,'gra', 'data', 'zadania.json')
    try:
        with open(file_path, 'r') as file:
            tasks = json.load(file)
    except FileNotFoundError:
        tasks = []
    if tasks:
        current_task = tasks[0]
    else:
        current_task = {}
    
    if request.method == 'POST':
        form = CommandForm(request.POST)
        if 'clear_button' in request.POST:
            return render(request, 'execute_command.html', {'form': form, 'title': current_task.get('title', ''), 'content': current_task.get('content', '')})
        elif form.is_valid():
            command = form.cleaned_data['command']
            result = execute_user_code(command)
            return render(request, 'execute_command.html', {'result': result, 'command': command, 'title': current_task.get('title', ''), 'content': current_task.get('content', '')})
    else:
        form = CommandForm()
    return render(request, 'execute_command.html', {'form': form, 'title': current_task.get('title', ''), 'content': current_task.get('content', '')})