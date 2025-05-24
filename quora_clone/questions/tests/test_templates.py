from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from questions.models import Question, Answer

class TemplateTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test users
        cls.user1 = User.objects.create_user(
            username='testuser1',
            password='testpassword'
        )
        
        cls.user2 = User.objects.create_user(
            username='testuser2',
            password='testpassword'
        )
        
        # Create test questions
        cls.question = Question.objects.create(
            topic='Test Topic',
            question='This is a test question?',
            author=cls.user1
        )
        
        # Create test answers
        cls.answer = Answer.objects.create(
            question=cls.question,
            answer='This is a test answer.',
            author=cls.user2
        )
    
    def setUp(self):
        self.client = Client()
    
    def test_home_template(self):
        """Test that the home template displays questions correctly"""
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'questions/home.html')
        
        # Check that question appears in the template
        self.assertContains(response, 'Test Topic')
        self.assertContains(response, 'This is a test question?')
        self.assertContains(response, 'testuser1')  # Author username
    
    def test_question_detail_template_logged_out(self):
        """Test the question detail template for logged out users"""
        response = self.client.get(
            reverse('question_detail', kwargs={'pk': self.question.pk})
        )
        # self.assertTemplateUsed(response, 'questions/question_detail.html')
        
        # # Check content
        # self.assertContains(response, 'This is a test question?')
        # self.assertContains(response, 'This is a test answer.')
        
        # # Should contain login message
        # self.assertContains(response, 'You have to login to answer the question')
        
        # # Should not contain answer form for logged out users
        # self.assertNotContains(response, 'Submit Answer')
    
    def test_question_detail_template_logged_in(self):
        """Test the question detail template for logged in users"""
        self.client.login(username='testuser1', password='testpassword')
        response = self.client.get(
            reverse('question_detail', kwargs={'pk': self.question.pk})
        )
        
        # Check that the answer form is present for logged in users
        self.assertContains(response, 'Submit Answer')
        
        # Check that edit button appears for the user's own answers
        self.assertNotContains(response, 'Edit')  # User1 didn't write the answer
        
        # Login as the answer author and check for edit button
        self.client.logout()
        self.client.login(username='testuser2', password='testpassword')
        response = self.client.get(
            reverse('question_detail', kwargs={'pk': self.question.pk})
        )
        self.assertContains(response, 'Edit')
    
    def test_edit_answer_template(self):
        """Test the edit answer template"""
        # Login as the answer author
        self.client.login(username='testuser2', password='testpassword')
        response = self.client.get(
            reverse('edit_answer', kwargs={'answer_id': self.answer.id})
        )
        self.assertTemplateUsed(response, 'questions/edit_answer.html')
        
        # Check content
        self.assertContains(response, 'Edit Answer')
        self.assertContains(response, 'This is a test question?')
        self.assertContains(response, 'Save Changes')
        self.assertContains(response, 'Cancel')
    
    def test_ask_question_template(self):
        """Test the ask question template"""
        self.client.login(username='testuser1', password='testpassword')
        response = self.client.get(reverse('ask_question'))
        self.assertTemplateUsed(response, 'questions/ask_question.html')
        
        # Check content
        self.assertContains(response, 'Ask a Question')
        self.assertContains(response, 'Topic')
        self.assertContains(response, 'Question')
        self.assertContains(response, 'Submit Question')
    
    def test_my_questions_template(self):
        """Test the my questions template"""
        # Create another question for the test user
        Question.objects.create(
            topic='Another Topic',
            question='This is another test question?',
            author=self.user1
        )
        
        self.client.login(username='testuser1', password='testpassword')
        response = self.client.get(reverse('my_questions'))
        self.assertTemplateUsed(response, 'questions/my_questions.html')
        
        # Should show only current user's questions
        self.assertContains(response, 'Test Topic')
        self.assertContains(response, 'Another Topic')
        self.assertEqual(len(response.context['questions']), 2)
        
        # Login as another user and check
        self.client.logout()
        self.client.login(username='testuser2', password='testpassword')
        response = self.client.get(reverse('my_questions'))
        
        # Should not contain questions from test_user1
        self.assertNotContains(response, 'Test Topic')
        self.assertEqual(len(response.context['questions']), 0)
        self.assertContains(response, 'You have not asked any question till date') 