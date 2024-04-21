from rest_framework import serializers
from .models import TextData

class TextSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    text = serializers.CharField(max_length = 255)
    video_duration = serializers.DecimalField(max_digits=10, decimal_places=3)


class WordBankSerializer(serializers.Serializer):
    # id = serializers.IntegerField()
    word = serializers.CharField()
    count = serializers.IntegerField()
    
class TextForWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextData
        fields = ['id', 'text', 'video_duration', 'video_url']
    

    video_url = serializers.SerializerMethodField(method_name='get_video_url')

    def get_video_url(self, textData: TextData):
        request = self.context.get('request')
        video_url = textData['video_link']
        return request.build_absolute_uri(video_url)

    # text = serializers.CharField(max_length = 255)
    # video_link = serializers.URLField()