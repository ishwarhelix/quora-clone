from django.test import TestCase
from django.contrib.auth.models import User
from questions.models import Question, Answer

class QuestionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user for the tests
        test_user = User.objects.create_user(
            username='testuser', 
            password='testpassword'
        )
        
        # Create a test question
        cls.question = Question.objects.create(
            topic='Test Topic',
            question='This is a test question?',
            author=test_user
        )
    
    def test_topic_max_length(self):
        max_length = self.question._meta.get_field('topic').max_length
        self.assertEqual(max_length, 200)
    
    def test_question_string_representation(self):
        self.assertEqual(str(self.question), self.question.question)
    
    def test_question_has_author(self):
        self.assertEqual(self.question.author.username, 'testuser')

class AnswerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user for the tests
        test_user = User.objects.create_user(
            username='testuser', 
            password='testpassword'
        )
        
        # Create another user for the likes
        cls.like_user = User.objects.create_user(
            username='likeuser', 
            password='testpassword'
        )
        
        # Create a test question
        cls.question = Question.objects.create(
            topic='Test Topic',
            question='This is a test question?',
            author=test_user
        )
        
        # Create a test answer
        cls.answer = Answer.objects.create(
            question=cls.question,
            answer='This is a test answer.',
            author=test_user
        )
    
    def test_answer_string_representation(self):
        expected_str = f'Answer by testuser on This is a test question?'
        self.assertEqual(str(self.answer), expected_str)
    
    def test_answer_has_author(self):
        self.assertEqual(self.answer.author.username, 'testuser')
    
    def test_answer_belongs_to_question(self):
        self.assertEqual(self.answer.question, self.question)
    
    def test_answer_likes(self):
        # Test adding a like
        self.answer.likes.add(self.like_user)
        self.assertEqual(self.answer.likes.count(), 1)
        self.assertTrue(self.like_user in self.answer.likes.all())
        
        # Test removing a like
        self.answer.likes.remove(self.like_user)
        self.assertEqual(self.answer.likes.count(), 0) 