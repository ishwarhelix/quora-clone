from django import forms
from .models import Question, Answer

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['topic', 'question']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer'] 