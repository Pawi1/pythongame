from django import forms

class CommandForm(forms.Form):
    command = forms.CharField(label='Wprowadź komendę', max_length=500)