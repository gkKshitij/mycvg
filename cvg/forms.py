from django import forms
from django.contrib.auth.models import User
from .models import Academics, Cv, Comment

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit#, Layout, Field
# from crispy_forms.bootstrap import (
#     PrependedText, PrependedAppendedText, FormActions
# )

class Cvform(forms.ModelForm):
    class Meta:
        model = Cv
        exclude=('published_date','created_by','edited_by','sap_id')
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'forms-control input-group-text', 'placeholder': 'Kshitij' }),
        }
        

class Academicsform(forms.ModelForm):
    class Meta:
        model = Academics
        exclude = ('cv','created_date','approved')
        

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