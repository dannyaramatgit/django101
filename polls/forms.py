from django import forms
from django.core import validators
from .models import Question, Choice
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

def validateCleanLang(value):
    CURSES = ('dumbass','moron')    
    for curse in CURSES:
        if curse in value:
            # self.add_error('question_text','Bad word detected')
            raise forms.ValidationError("Bad word detected")
    return value

class QuestionForm(forms.ModelForm):
    question_text = forms.CharField(label="Question Text", max_length=200, validators=[validateCleanLang])
    # pub_date = forms.DateTimeField(label='Date Published', input_formats=['%Y-%m-%d %h:%m:%s'])
    class Meta:
        model = Question
        fields = '__all__'
            
    def clean(self):
        CURSES = ('dumbass','moron')
        super().clean()
        for curse in CURSES:
            if curse in self.cleaned_data['question_text']:
                self.add_error('question_text', 'second added error')
                raise forms.ValidationError("Bad word detected")
        return self.cleaned_data


class ChoiceForm(forms.ModelForm):
    # choice_text = forms.CharField(label="answer text", max_length=20)
    # votes = forms.IntegerField(label="no of votes", initial=0)
    # question = forms.ModelChoiceField(queryset=Question.objects.all())
    class Meta:
        model=Choice
        fields = '__all__'
        # exclude = ['votes']
        labels = {
            'choice_text':_('Answer text'),
            'votes': 'number of votes'
        }
        error_messages = {
            'choice_text' : {'required': "this is way too long"}
            }

    def clean(self):
        CURSES = ('dumbass','moron')
        super().clean()
        errors = []
        for curse in CURSES:
            if curse in self.cleaned_data['choice_text']:
                self.add_error('choice_text', 'Bad word detected')
                errors.append(forms.ValidationError("Bad word detected"))
        if self.cleaned_data['votes'] < 0:
            errors.append(("Votes most be 0 or higher"))

        if len(errors) > 0:
            raise errors
        return self.cleaned_data


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'is_active']

class LoginForm(forms.Form):
    username = forms.CharField(label="User Name", required=True)
    password = forms.CharField(
            widget=forms.PasswordInput(attrs={
                'placeholder': _('Current Password')
            }),
            error_messages={
                'required': _('Please enter your current password.')
            }) 