from django.db import models
from django.utils import timezone
import datetime
from django.core import validators
import django.forms as forms

def validateCleanLang(value):
    CURSES = ('dumbass','moron')    
    for curse in CURSES:
        if curse in value:
            # self.add_error('question_text','Bad word detected')
            raise forms.ValidationError("Bad word detected")
    return value
           

class Question(models.Model):
    question_text = models.CharField('Question', max_length=200, validators=[validateCleanLang, validators.MinLengthValidator(5)])
    pub_date = models.DateTimeField('Date published')

    def was_published_lately(self):
        return self.pub_date >= timezone.now()-datetime.timedelta(days=1)

    def __str__(self) -> str:
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=20)
    votes = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.choice_text