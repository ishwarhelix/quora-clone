from django.test import SimpleTestCase
from django.urls import reverse, resolve
from questions.views import (
    home, 
    ask_question, 
    question_detail, 
    like_answer, 
    myquestions, 
    edit_answer
)

class UrlsTest(SimpleTestCase):
    def test_home_url_resolves(self):
        url = reverse('home')
        self.assertEqual(url, '/')
        self.assertEqual(resolve(url).func, home)
    
    def test_ask_question_url_resolves(self):
        url = reverse('ask_question')
        self.assertEqual(url, '/ask/')
        self.assertEqual(resolve(url).func, ask_question)
    
    def test_question_detail_url_resolves(self):
        url = reverse('question_detail', args=[1])
        self.assertEqual(url, '/question/1/')
        self.assertEqual(resolve(url).func, question_detail)
    
    def test_like_answer_url_resolves(self):
        url = reverse('like_answer', args=[1])
        self.assertEqual(url, '/like/1/')
        self.assertEqual(resolve(url).func, like_answer)
    
    def test_my_questions_url_resolves(self):
        url = reverse('my_questions')
        self.assertEqual(url, '/myquestions/')
        self.assertEqual(resolve(url).func, myquestions)
    
    def test_edit_answer_url_resolves(self):
        url = reverse('edit_answer', args=[1])
        self.assertEqual(url, '/answer/1/edit/')
        self.assertEqual(resolve(url).func, edit_answer) 