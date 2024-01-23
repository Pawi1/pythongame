from django.shortcuts import render
import ast
import sys
from .forms import CommandForm
from io import StringIO
from resource import setrlimit,RLIMIT_CPU
def execute_command(request):
    if request.method == 'POST':
        form = CommandForm(request.POST)
        if form.is_valid():
            command = form.cleaned_data['command']
            try:
                parsed_command = ast.parse(command, mode='exec')
                compiled_code = compile(parsed_command, '<string>', 'exec')
                original_stdout = sys.stdout
                sys.stdout = result_buffer = StringIO()
                globals_parameter = {'__builtins__': None}
                locals_parameter = {
                    'print': print,
                    'input': input,
                    'int': int,
                    'float': float,
                    'str': str,
                    'list': list,
                    'tuple': tuple,
                    'dict': dict,
                    'set': set,
                    'bool': bool,
                    'len': len,
                    'range': range,
                    'sum': sum,
                    'abs': abs,
                    'max': max,
                    'min': min,
                    'sorted': sorted,
                    'enumerate': enumerate,
                    'zip': zip,
                    'map': map,
                    'filter': filter,
                    'all': all,
                    'any': any,
                    'dir': dir,
                    'iter': iter
                }                
                setrlimit(RLIMIT_CPU,(15, 15))
                exec(compiled_code, globals_parameter, locals_parameter)
                sys.stdout = original_stdout
                return render(request, 'execute_command.html', {'result': result_buffer.getvalue()})
            except SyntaxError as e:
                error_message = "Błąd składni: {}".format(str(e))
                return render(request, 'execute_command.html', {'error_message': error_message})
            except Exception as e:
                error_message = "Błąd: {}".format(str(e))
                return render(request, 'execute_command.html', {'error_message': error_message})
    else:
        form = CommandForm()
    return render(request, 'execute_command.html', {'form': form})