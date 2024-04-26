from django.db import models

# Create your models here.

class TextData(models.Model):
    text = models.TextField()
    video_link = models.URLField(max_length=200)
    video_duration = models.DecimalField(max_digits=10, decimal_places=3)

class PartOfSpeach(models.Model):
    pos = models.CharField(max_length=20)

class Homophone(models.Model):
    homophone = models.CharField(max_length = 50)
    homophone_group_id = models.PositiveIntegerField(default=0)

class WordDetail(models.Model):
    text = models.ForeignKey(TextData, on_delete=models.CASCADE)
    homophone = models.ForeignKey(Homophone, on_delete=models.DO_NOTHING)
    pos = models.ForeignKey(PartOfSpeach, on_delete=models.DO_NOTHING)
    word = models.CharField(max_length=50)
    start_time = models.DecimalField(max_digits=10, decimal_places=3)
    end_time = models.DecimalField(max_digits=10, decimal_places=3)
    word_duration = models.DecimalField(max_digits=10, decimal_places=3)
    difficulty = models.CharField(max_length=7, blank=False, default='empty')
    positive = models.BooleanField(default=False)
    negative = models.BooleanField(default=False)