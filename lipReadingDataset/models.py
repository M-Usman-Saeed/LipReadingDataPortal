from django.db import models

# Create your models here.

class TextData(models.Model):
    GENDERS = [
        ('M', 'Male'),
        ('F', 'Female')
    ]
    text = models.TextField()
    gender = models.CharField(max_length=1, choices=GENDERS)
    race = models.CharField(max_length=50)

class VideoData(models.Model):
    text_id = models.OneToOneField(TextData, on_delete=models.CASCADE, primary_key=True)
    video_link = models.URLField()
    duration = models.DurationField()

class WordDetails(models.Model):
    text_id = models.ForeignKey(TextData, on_delete=models.DO_NOTHING)
    word = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()