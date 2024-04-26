from django.urls import path, include
from . import views

urlpatterns = [
    path('hello/', views.say_hello),
    path('word-Bank/', views.word_bank_data),
    path('wordBank/', views.word_bank),
    path('text-detail/<int:id>/', views.text_detail),
    path('text_for_word/', views.textForWord),
]