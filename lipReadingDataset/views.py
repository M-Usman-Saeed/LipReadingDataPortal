from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import TextData, WordDetail, Homophone
from django.db.models import Count, Q
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import TextSerializer, WordBankSerializer, TextForWordSerializer

# Create your views here.

def word_bank_data(request):
    words = WordDetail.objects.values('word') \
                            .annotate(word_count=Count('word')) \
                            .order_by('-word_count')[:10]
    word_list = list(words)
    return JsonResponse({'words': word_list})

@api_view()
def text_detail(request, id):
    print(id)
    text = get_object_or_404(TextData, pk=id)
    serializer = TextSerializer(text)
    return Response(serializer.data)


# @api_view()
# def textForWord(request):
#     # Retrieve the search word from query parameters
#     word = request.query_params.get('word', None)  # Default to None if not provided

#     if not word:
#         return Response(
#             {"error": "Missing 'word' parameter."},
#             status=status.HTTP_400_BAD_REQUEST,
#         )
    
#     # Retrieve the range start and end for word_duration from query parameters
#     duration_start = request.query_params.get('duration_start', None)
#     duration_end = request.query_params.get('duration_end', None)

#     # Start with a base query for texts that contain the specified word
#     text_filter = Q(worddetail__word=word)

#     # If both duration_start and duration_end are provided and valid, use them to create the range
#     if duration_start is not None and duration_end is not None:
#         try:
#             # Convert them to floats to ensure they're valid numbers
#             duration_start = float(duration_start)
#             duration_end = float(duration_end)
            
#             # Update the query filter to include the range
#             text_filter &= Q(
#                 worddetail__word_duration__gte=duration_start,
#                 worddetail__word_duration__lte=duration_end
#             )
#         except ValueError:
#             # Return a bad request response if the values cannot be converted to float
#             return Response(
#                 {"error": "Invalid duration_start or duration_end format. They should be numbers."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#     # Get the filtered list of TextData
#     textList = TextData.objects.filter(text_filter).distinct().values(
#         'id', 'text', 'video_duration', 'video_link'
#     )

#     # Serialize and return the data
#     serializer = TextForWordSerializer(textList, many=True, context={'request': request})
#     return Response(serializer.data)


@api_view(['GET'])
def textForWord(request):
    # Retrieve query parameters
    word = request.query_params.get('word', None)
    homophone_word = request.query_params.get('homophone', None)  # Homophone word parameter
    positive = request.query_params.get('positive', None)
    negative = request.query_params.get('negative', None)

    # Check for missing required parameters
    if not word and not homophone_word and not positive and not negative:
        return Response(
            {"error": "Missing parameter."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    
    # Base query filter
    text_filter = Q()

    # If a specific word is provided, filter by texts containing that word
    if word:
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
                    {"error": "Invalid duration_start or duration_end format. They should be decimal numbers."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

    # If a homophone word is provided, retrieve its group and include all words from that group
    if homophone_word:
        homophone_group_id = Homophone.objects.filter(homophone=homophone_word).values_list("homophone_group_id", flat=True).first()
        if homophone_group_id:
            homophone_words = list(Homophone.objects.filter(homophone_group_id=homophone_group_id).values_list("homophone", flat=True))
            text_filter |= Q(worddetail__word__in=homophone_words)
        else:
            return Response(
                {"error": f"No homophones found for '{homophone_word}'"},
                status=status.HTTP_404_NOT_FOUND,
            )
        
    if positive:
        text_filter &= Q(worddetail__positive=positive)
    
    if negative:
        text_filter &= Q(worddetail__negative=negative)

    # Fetch the filtered list of TextData
    textList = TextData.objects.filter(text_filter).distinct().values(
        'id', 'text', 'video_duration', 'video_link'
    )[:10]

    # Serialize and return the data
    serializer = TextForWordSerializer(textList, many=True, context={'request': request})
    
    if serializer.data == []:
        return Response(
            {"error": f"No Text found for '{word}'"},
            status=status.HTTP_404_NOT_FOUND,
        )
    else:
        return Response(serializer.data)