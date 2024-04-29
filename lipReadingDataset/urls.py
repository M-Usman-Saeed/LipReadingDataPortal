from django.urls import path, include
from . import views

urlpatterns = [
    path('word-Bank/', views.word_bank_data),
    path('text_for_word/', views.textForWord),
]