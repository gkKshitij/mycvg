from django import forms
from django.contrib.auth.models import User
from .models import Student, Comment

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit#, Layout, Field
# from crispy_forms.bootstrap import (
#     PrependedText, PrependedAppendedText, FormActions
# )

class Studentform(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('title','text')

class Commentform(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        
class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    helper=FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('Sign up', 'Sign up', css_class='btn btn-primary'))
    class Meta:
        model = User
        fields = ('username', 'password', 'email')