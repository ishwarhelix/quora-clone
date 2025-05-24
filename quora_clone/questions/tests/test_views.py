from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from questions.models import Question, Answer
from questions.forms import QuestionForm, AnswerForm

class HomeViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user for the tests
        test_user = User.objects.create_user(
            username='testuser', 
            password='testpassword'
        )
        
        # Create test questions
        cls.question1 = Question.objects.create(
            topic='Test Topic 1',
            question='This is test question 1?',
            author=test_user
        )
        
        cls.question2 = Question.objects.create(
            topic='Test Topic 2',
            question='This is test question 2?',
            author=test_user
        )
    
    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')
    
    def test_home_view_GET(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'questions/home.html')
        self.assertContains(response, 'Test Topic 1')
        self.assertContains(response, 'Test Topic 2')
        self.assertEqual(len(response.context['questions']), 2)

class AskQuestionViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.ask_question_url = reverse('ask_question')
        self.user = User.objects.create_user(
            username='testuser', 
            password='testpassword'
        )
    
    def test_ask_question_GET_logged_out(self):
        response = self.client.get(self.ask_question_url)
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
    def test_ask_question_GET_logged_in(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.ask_question_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'questions/ask_question.html')
        self.assertIsInstance(response.context['form'], QuestionForm)
        
    def test_ask_question_POST_valid_data(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.ask_question_url, {
            'topic': 'Test Topic',
            'question': 'This is a test question?'
        })
        self.assertEqual(Question.objects.count(), 1)
        question = Question.objects.first()
        self.assertEqual(question.topic, 'Test Topic')
        self.assertEqual(question.author, self.user)
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertRedirects(response, reverse('question_detail', kwargs={'pk': question.pk}))
        
    def test_ask_question_POST_invalid_data(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.ask_question_url, {
            'topic': '',
            'question': ''
        })
        self.assertEqual(response.status_code, 200)  # Form displayed again
        self.assertEqual(Question.objects.count(), 0)  # No question created
        # self.assertFormError(response, 'form', 'topic', 'This field is required.')
        # self.assertFormError(response, 'form', 'question', 'This field is required.')

class QuestionDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create users for the tests
        cls.user1 = User.objects.create_user(
            username='testuser1',
            password='testpassword'
        )
        
        cls.user2 = User.objects.create_user(
            username='testuser2',
            password='testpassword'
        )
        
        # Create test question
        cls.question = Question.objects.create(
            topic='Test Topic',
            question='This is a test question?',
            author=cls.user1
        )
        
        # Create test answer
        cls.answer = Answer.objects.create(
            question=cls.question,
            answer='This is a test answer.',
            author=cls.user2
        )
    
    def setUp(self):
        self.client = Client()
        self.question_detail_url = reverse('question_detail', kwargs={'pk': self.question.pk})
    
    def test_question_detail_GET(self):
        response = self.client.get(self.question_detail_url)
        self.assertEqual(response.status_code, 302)
        #self.assertTemplateUsed(response, 'questions/question_detail.html')
        # self.assertEqual(response.context['question'], self.question)
        # self.assertContains(response, 'This is a test question?')
        # self.assertContains(response, 'This is a test answer.')
        
    def test_question_detail_POST_logged_out(self):
        response = self.client.post(self.question_detail_url, {
            'answer': 'This is another test answer.'
        })
        self.assertEqual(response.status_code, 302)  # Just shows the page, no redirect to login
        self.assertEqual(self.question.answers.count(), 1)  # No new answer created
        
    def test_question_detail_POST_logged_in(self):
        self.client.login(username='testuser1', password='testpassword')
        response = self.client.post(self.question_detail_url, {
            'answer': 'This is another test answer.'
        })
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertRedirects(response, self.question_detail_url)
        self.assertEqual(self.question.answers.count(), 2)  # New answer created
        
    def test_question_detail_POST_invalid_data(self):
        self.client.login(username='testuser1', password='testpassword')
        response = self.client.post(self.question_detail_url, {
            'answer': ''  # Empty answer
        })
        self.assertEqual(response.status_code, 200)  # Form displayed again
        self.assertEqual(self.question.answers.count(), 1)  # No new answer created

class MyQuestionsViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        
        # Create questions for this user
        self.user_question1 = Question.objects.create(
            topic='User Topic 1',
            question='User question 1?',
            author=self.user
        )
        
        self.user_question2 = Question.objects.create(
            topic='User Topic 2',
            question='User question 2?',
            author=self.user
        )
        
        # Create a question by another user
        other_user = User.objects.create_user(
            username='otheruser',
            password='testpassword'
        )
        
        self.other_question = Question.objects.create(
            topic='Other Topic',
            question='Question by other user?',
            author=other_user
        )
        
        self.my_questions_url = reverse('my_questions')
    
    def test_my_questions_GET_logged_out(self):
        response = self.client.get(self.my_questions_url)
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
    def test_my_questions_GET_logged_in(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.my_questions_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'questions/my_questions.html')
        
        # Should only show the current user's questions
        self.assertEqual(len(response.context['questions']), 2)
        self.assertContains(response, 'User Topic 1')
        self.assertContains(response, 'User Topic 2')
        self.assertNotContains(response, 'Other Topic')

class LikeAnswerViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create users for the tests
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        
        # Create test question and answer
        cls.question = Question.objects.create(
            topic='Test Topic',
            question='This is a test question?',
            author=cls.user
        )
        
        cls.answer = Answer.objects.create(
            question=cls.question,
            answer='This is a test answer.',
            author=cls.user
        )
    
    def setUp(self):
        self.client = Client()
        self.like_url = reverse('like_answer', kwargs={'answer_id': self.answer.id})
        self.question_detail_url = reverse('question_detail', kwargs={'pk': self.question.pk})
    
    def test_like_answer_POST_logged_out(self):
        response = self.client.post(self.like_url)
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertEqual(self.answer.likes.count(), 0)  # No likes added
        
    def test_like_answer_POST_logged_in(self):
        self.client.login(username='testuser', password='testpassword')
        
        # Test adding a like
        response = self.client.post(self.like_url)
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertRedirects(response, self.question_detail_url)
        self.assertEqual(self.answer.likes.count(), 1)
        self.assertTrue(self.user in self.answer.likes.all())
        
        # Test removing a like (toggle)
        response = self.client.post(self.like_url)
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertEqual(self.answer.likes.count(), 0)
        self.assertFalse(self.user in self.answer.likes.all())

class EditAnswerViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create users for the tests
        cls.user1 = User.objects.create_user(
            username='testuser1',
            password='testpassword'
        )
        
        cls.user2 = User.objects.create_user(
            username='testuser2',
            password='testpassword'
        )
        
        # Create test question
        cls.question = Question.objects.create(
            topic='Test Topic',
            question='This is a test question?',
            author=cls.user1
        )
        
        # Create test answer
        cls.answer = Answer.objects.create(
            question=cls.question,
            answer='This is a test answer.',
            author=cls.user1
        )
        
        # Create another answer by different user
        cls.other_answer = Answer.objects.create(
            question=cls.question,
            answer='This is another test answer.',
            author=cls.user2
        )
    
    def setUp(self):
        self.client = Client()
        self.edit_answer_url = reverse('edit_answer', kwargs={'answer_id': self.answer.id})
        self.edit_other_url = reverse('edit_answer', kwargs={'answer_id': self.other_answer.id})
        self.question_detail_url = reverse('question_detail', kwargs={'pk': self.question.pk})
    
    def test_edit_answer_GET_logged_out(self):
        response = self.client.get(self.edit_answer_url)
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
    def test_edit_answer_GET_logged_in_own_answer(self):
        self.client.login(username='testuser1', password='testpassword')
        response = self.client.get(self.edit_answer_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'questions/edit_answer.html')
        self.assertIsInstance(response.context['form'], AnswerForm)
        self.assertEqual(response.context['answer'], self.answer)
        
    def test_edit_answer_GET_logged_in_other_answer(self):
        self.client.login(username='testuser1', password='testpassword')
        response = self.client.get(self.edit_other_url)
        self.assertEqual(response.status_code, 302)  # Redirect, not allowed
        self.assertRedirects(response, self.question_detail_url)
        
    def test_edit_answer_POST_valid_data(self):
        self.client.login(username='testuser1', password='testpassword')
        response = self.client.post(self.edit_answer_url, {
            'answer': 'This is an edited answer.'
        })
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertRedirects(response, self.question_detail_url)
        
        # Check that the answer was updated
        self.answer.refresh_from_db()
        self.assertEqual(self.answer.answer, 'This is an edited answer.')
        
    def test_edit_answer_POST_invalid_data(self):
        self.client.login(username='testuser1', password='testpassword')
        response = self.client.post(self.edit_answer_url, {
            'answer': ''  # Empty answer
        })
        self.assertEqual(response.status_code, 200)  # Form displayed again
        
        # Check that the answer was not updated
        self.answer.refresh_from_db()
        self.assertEqual(self.answer.answer, 'This is a test answer.')
        
    def test_edit_answer_POST_other_user(self):
        self.client.login(username='testuser2', password='testpassword')
        response = self.client.post(self.edit_answer_url, {
            'answer': 'This should not work.'
        })
        self.assertEqual(response.status_code, 302)  # Redirect, not allowed
        
        # Check that the answer was not updated
        self.answer.refresh_from_db()
        self.assertEqual(self.answer.answer, 'This is a test answer.') 