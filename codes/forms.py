from dataclasses import fields
from django import forms
from .models import Code

class CodeForm(forms.ModelForm):
    number = forms.CharField(label='code', help_text='Enter sms verification code')
    class Meta:
        model = Code
        fields = ('number',)