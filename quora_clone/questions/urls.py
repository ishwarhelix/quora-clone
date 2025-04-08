from django.urls import path
from .import   views

urlpatterns = [
    path('', views.home, name='home'),
    path('ask/', views.ask_question, name='ask_question'),
    path('question/<int:pk>/', views.question_detail, name='question_detail'),
    path('like/<int:answer_id>/', views.like_answer, name='like_answer'),
    path('myquestions/', views.myquestions, name='my_questions'),
    path('answer/<int:answer_id>/edit/', views.edit_answer, name='edit_answer'),
] 