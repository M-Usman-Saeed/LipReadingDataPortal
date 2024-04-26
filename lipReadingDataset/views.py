from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import TextData, WordDetail
from django.db.models import Count, Q
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

# @api_view()
# def textForWord(request, word):
#     textList = TextData.objects.filter(
#         Q(worddetail__word = word)
#     ).values('id', 'text', 'video_duration', 'video_link')[:5]
#     serializer = TextForWordSerializer(textList, many=True, context={'request': request})
#     return Response(serializer.data)


@api_view()
def textForWord(request):
    # Retrieve the search word from query parameters
    word = request.query_params.get('word', None)  # Default to None if not provided

    if not word:
        return Response(
            {"error": "Missing 'word' parameter."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    
    # Retrieve the range start and end for word_duration from query parameters
    duration_start = request.query_params.get('duration_start', None)
    duration_end = request.query_params.get('duration_end', None)

    # Start with a base query for texts that contain the specified word
    text_filter = Q(worddetail__word=word)

    # If both duration_start and duration_end are provided and valid, use them to create the range
    if duration_start is not None and duration_end is not None:
        try:
            # Convert them to floats to ensure they're valid numbers
            duration_start = float(duration_start)
            duration_end = float(duration_end)
            
            # Update the query filter to include the range
            text_filter &= Q(
                worddetail__word_duration__gte=duration_start,
                worddetail__word_duration__lte=duration_end
            )
        except ValueError:
            # Return a bad request response if the values cannot be converted to float
            return Response(
                {"error": "Invalid duration_start or duration_end format. They should be numbers."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    # Get the filtered list of TextData
    textList = TextData.objects.filter(text_filter).distinct().values(
        'id', 'text', 'video_duration', 'video_link'
    )

    # Serialize and return the data
    serializer = TextForWordSerializer(textList, many=True, context={'request': request})
    return Response(serializer.data)