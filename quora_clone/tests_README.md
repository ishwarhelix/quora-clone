# Quora Clone Test Suite

This project includes a comprehensive test suite that verifies all the functionality of the Quora Clone application. The tests cover models, forms, views, URLs, and templates.

## Test Structure

The test suite is organized as follows:

### Accounts App Tests
- `accounts/tests.py` - Tests for user registration, login, and logout functionality

### Questions App Tests
- `questions/tests/test_models.py` - Tests for Question and Answer models
- `questions/tests/test_forms.py` - Tests for QuestionForm and AnswerForm
- `questions/tests/test_views.py` - Tests for all view functions
- `questions/tests/test_urls.py` - Tests for URL patterns and resolution
- `questions/tests/test_templates.py` - Tests for template rendering and content

## Running the Tests

To run the complete test suite:

```bash
python manage.py test
```

To run specific test files:

```bash
python manage.py test accounts.tests  # Run only accounts app tests
python manage.py test questions.tests.test_models  # Run only model tests
python manage.py test questions.tests.test_views  # Run only view tests
python manage.py test questions.tests.test_forms  # Run only form tests
python manage.py test questions.tests.test_urls  # Run only URL tests
python manage.py test questions.tests.test_templates  # Run only template tests
```

To run a specific test case:

```bash
python manage.py test questions.tests.test_views.QuestionDetailViewTest
```

To run a specific test method:

```bash
python manage.py test questions.tests.test_views.QuestionDetailViewTest.test_question_detail_GET
```

## Test Coverage

These tests cover the following functionality:

1. **User Authentication**:
   - User registration with valid/invalid data
   - User login with valid/invalid credentials
   - User logout

2. **Questions**:
   - Creating questions
   - Viewing questions
   - Listing user's own questions

3. **Answers**:
   - Creating answers
   - Editing answers (only by the author)
   - Liking/unliking answers

4. **Security and Permissions**:
   - Access restrictions for logged-out users
   - Permission enforcement for editing answers
   - Protection against unauthorized modifications

## Continuous Integration

It's recommended to run these tests before deploying any changes to ensure that new code doesn't break existing functionality.

## Test Database

Tests run on a separate database from your development or production databases, so your real data is never affected by the tests. 