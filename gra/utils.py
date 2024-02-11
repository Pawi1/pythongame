from resource import setrlimit,RLIMIT_CPU
import ast
import sys
from io import StringIO
import json
from gra import crypto
from django.shortcuts import redirect
from django.shortcuts import render
def execute_user_code(command):
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
        setrlimit(RLIMIT_CPU, (15, 15))
        exec(compiled_code, globals_parameter, locals_parameter)
        sys.stdout = original_stdout
        result = result_buffer.getvalue()
        return result
    except SyntaxError as e:
        error_message = "Błąd składni: {}".format(str(e))
        return error_message
    except Exception as e:
        error_message = "Błąd: {}".format(str(e))
        return error_message
def open_file(file_path):    
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
    return data
def get_level(request):
    if not request.COOKIES.get('level'):
        return 0
    level = crypto.decrypt_data(request.COOKIES.get('level'))
    return int(level)
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