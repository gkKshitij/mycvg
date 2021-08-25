from django import forms
from django.contrib.auth.models import User
from .models import Academics, Cv, Comment, Skills, Projects, Internships, Extracurricular, Roles

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit  # , Layout, Field


# from crispy_forms.bootstrap import (
#     PrependedText, PrependedAppendedText, FormActions
# )


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('Sign up', 'Sign up', css_class='btn btn-primary'))

    class Meta:
        model = User
        fields = ('username', 'password', 'email')


class Cvform(forms.ModelForm):
    class Meta:
        model = Cv
        exclude = ('published_date', 'created_by', 'edited_by', 'sap_id', 'modified_date')
        # widgets = {
        #     'first_name': forms.TextInput(attrs={'class': 'forms-control input-group-text', }),
        # }


class Academicsform(forms.ModelForm):
    class Meta:
        model = Academics
        exclude = ('cv', 'approved', 'edited_by', 'modified_date')


class Skillsform(forms.ModelForm):
    class Meta:
        model = Skills
        exclude = ('cv', 'approved', 'edited_by', 'modified_date')


class Extracurricularform(forms.ModelForm):
    class Meta:
        model = Extracurricular
        exclude = ('cv', 'approved', 'edited_by', 'modified_date')


class Internshipsform(forms.ModelForm):
    class Meta:
        model = Internships
        exclude = ('cv', 'approved', 'edited_by', 'modified_date')


class Projectsform(forms.ModelForm):
    class Meta:
        model = Projects
        exclude = ('cv', 'approved', 'edited_by', 'modified_date')


class Rolesform(forms.ModelForm):
    class Meta:
        model = Roles
        exclude = ('cv', 'approved', 'edited_by', 'modified_date')


class Commentform(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)



