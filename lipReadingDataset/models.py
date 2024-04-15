from django.db import models

# Create your models here.

class TextData(models.Model):
    text = models.TextField()
    video_link = models.URLField(max_length=200, null=True)
    video_duration = models.DecimalField(max_digits=10, decimal_places=3, null=True)

class PartOfSpeach(models.Model):
    pos = models.CharField(max_length=20)

class WordDetail(models.Model):
    text_id = models.ForeignKey(TextData, on_delete=models.DO_NOTHING)
    word = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()
    word_duration = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    pos_id = models.OneToOneField(PartOfSpeach, on_delete=models.CASCADE)
    difficulty = models.CharField(max_length=7)
    positive = models.BooleanField()
    negative = models.BooleanField()

class Homephone(models.Model):
    word_id = models.ForeignKey(WordDetail, on_delete=models.DO_NOTHING)
    homophone = models.CharField(max_length = 50)