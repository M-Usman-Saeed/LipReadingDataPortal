from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import TextData, WordDetail
from django.db.models import Count
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import TextSerializer, WordBankSerializer, TextForWordSerializer

# Create your views here.

def say_hello(request):
    # query_set = TextData.objects.all()

    # query_set = TextData.objects.filter(
    #     worddetail__word='should'
    # ).values('text', 'video_link')

    query_set = WordDetail.objects.values('word') \
                            .annotate(word_count=Count('word')) \
                            .order_by('-word_count')

    # query_set.filter().

    # for text in query_set:
    #     print(text)

    # return render(request, 'home.html', {'name':'Usman', 'texts':list(query_set)})
    return render(request, 'word_bank.html', {'name':'Usman', 'texts':list(query_set)})


def word_bank_data(request):
    # words = WordDetail.objects.all().values_list('word', flat=True)
    # word_list = list(words)
    words = WordDetail.objects.values('word') \
                            .annotate(word_count=Count('word')) \
                            .order_by('-word_count')[:10]
    word_list = list(words)
    return JsonResponse({'words': word_list})

@api_view()
def word_bank(request):
    wordDetails = WordDetail.objects.values('word') \
                            .annotate(word_count=Count('word')) \
                            .order_by('-word_count')
    serializer = WordBankSerializer(wordDetails)
    return Response(serializer.data)

@api_view()
def text_detail(request, id):
    print(id)
    text = get_object_or_404(TextData, pk=id)
    serializer = TextSerializer(text)
    return Response(serializer.data)

@api_view()
def textForWord(request, word):
    textList = TextData.objects.filter(
        worddetail__word = word
    ).values('id', 'text', 'video_duration', 'video_link')[:5]
    serializer = TextForWordSerializer(textList, many=True, context={'request': request})
    print(serializer.data)
    return Response(serializer.data)