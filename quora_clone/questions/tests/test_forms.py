from django.test import TestCase
from questions.forms import QuestionForm, AnswerForm

class QuestionFormTest(TestCase):
    def test_question_form_valid_data(self):
        form = QuestionForm({
            'topic': 'Test Topic',
            'question': 'This is a test question?'
        })
        self.assertTrue(form.is_valid())
    
    def test_question_form_no_data(self):
        form = QuestionForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)
        self.assertIn('topic', form.errors)
        self.assertIn('question', form.errors)
    
    def test_question_form_empty_topic(self):
        form = QuestionForm({
            'topic': '',
            'question': 'This is a test question?'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('topic', form.errors)
    
    def test_question_form_empty_question(self):
        form = QuestionForm({
            'topic': 'Test Topic',
            'question': ''
        })
        self.assertFalse(form.is_valid())
        self.assertIn('question', form.errors)

class AnswerFormTest(TestCase):
    def test_answer_form_valid_data(self):
        form = AnswerForm({
            'answer': 'This is a test answer.'
        })
        self.assertTrue(form.is_valid())
    
    def test_answer_form_no_data(self):
        form = AnswerForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertIn('answer', form.errors)
    
    def test_answer_form_empty_answer(self):
        form = AnswerForm({
            'answer': ''
        })
        self.assertFalse(form.is_valid())
        self.assertIn('answer', form.errors) 